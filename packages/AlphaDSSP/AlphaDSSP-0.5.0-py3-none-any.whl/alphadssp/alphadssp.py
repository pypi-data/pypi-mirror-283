import numpy as np
import tarfile
import gzip
import tempfile
import json
import pickle
import os
import time
import shutil
from io import StringIO
from multiprocessing import Pool
from functools import partial
from tqdm import trange
from Bio.PDB import MMCIFParser, DSSP

'''
Tar shards from Alphafold can be obtained by organism TaxID using the following command: 
`gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-[TAX ID]-*_v4.tar .`
'''

def get_structure_count(tar_paths, extension = ".cif.gz"):
    count = 0
    if isinstance(tar_paths, str):
        tar_paths = [tar_paths]

    for path in tar_paths:
        with tarfile.open(path, "r") as tar:
            for member in tar.getmembers():
                if member.name.endswith(extension):
                    count += 1

    return count

def stream_structures(tar_paths, chunk_size = 100):
    # Prompt user for paths if none are passed
    if tar_paths is None:
        tar_paths = []
        while True:
            if len(tar_paths) == 0:
                prompt = "Enter path to alphafold tar file or shard:  "
            else:
                prompt = "Enter another path, or hit enter when done:  "
            path = input(prompt)
            if path != "":
                tar_paths.append(path)
            else:
                break

    # Stream the structures as pairs of mmCIF and JSON files
    chunk = []
    parser = MMCIFParser(QUIET=True)  # Reuse parser to avoid repeated instantiation

    for tar_path in tar_paths:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract tar to a temporary directory
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(path=temp_dir)

            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith(".cif.gz"):
                        cif_path = os.path.join(root, file)

                        # Extract the mmCIF file
                        with gzip.open(cif_path, "rt", encoding="utf-8") as gz_text:
                            string_data = gz_text.read()

                        # Parse the file into a structure directly from string data
                        base_name = os.path.basename(file).split(".cif.gz")[0]
                        structure = parser.get_structure(base_name, StringIO(string_data))
                        model = structure[0]

                        # Write to a temporary file for DSSP processing
                        temp_cif_file = os.path.join(temp_dir, f"{base_name}.cif")
                        with open(temp_cif_file, "w") as temp_file:
                            temp_file.write(string_data)

                        # Extract the accompanying JSON file
                        confidence_json_name = file.replace(".cif.gz", ".json.gz").replace("model", "confidence")
                        confidence_json_path = os.path.join(root, confidence_json_name)
                        if os.path.exists(confidence_json_path):
                            with gzip.open(confidence_json_path, "rt") as gzip_file:
                                confidence_dict = json.load(gzip_file)
                                confidence_vals = np.array(confidence_dict["confidenceScore"])

                            chunk.append((temp_cif_file, model, base_name, confidence_vals))

                            if len(chunk) == chunk_size:
                                completed_chunk = chunk.copy()
                                chunk = []  # reset for next cycle
                                yield completed_chunk

    # Yield the last chunk if it's not empty
    if chunk:
        yield chunk

def run_dssp(entry_tuple, dssp_executable="/usr/bin/dssp", forbidden_codes = ("H","B","E","G","I","T"), plddt_thres=70):
    # Function for single entry; near maximum efficiency because DSSP() takes >99% of the elapsed time

    cif_file, model, base_name, plddt_vals = entry_tuple
    dssp = DSSP(model, cif_file, dssp=dssp_executable)
    dssp_codes = [val[2] for val in list(dssp.property_dict.values())]
    forbidden_dssp_mask = np.isin(dssp_codes, forbidden_codes)

    # Only consider forbidden secondary structures if model confidence passes a given threshold
    plddt_mask = np.greater_equal(plddt_vals, plddt_thres)
    high_confidence_forbidden = np.logical_and(plddt_mask, forbidden_dssp_mask)
    results = (high_confidence_forbidden, "".join(dssp_codes))
    os.unlink(cif_file)  # Remove the temporary file after use

    return (base_name, results)

def run_dssp_chunk(chunk, dssp_executable="/usr/bin/dssp", forbidden_codes = ("H","B","E","G","I","T"), plddt_thres=70):
    # Function for iterating through a chunk

    excluded_results_chunk = {}
    for entry_tuple in chunk:
        base_name, results = run_dssp(entry_tuple, dssp_executable, forbidden_codes, plddt_thres)
        excluded_results_chunk[base_name] = results

    return excluded_results_chunk

def run_dssp_parallel(tar_paths, dssp_executable="/usr/bin/dssp", forbidden_codes = ("H","B","E","G","I","T"),
                      plddt_thres=70, chunk_size = 100):

    print(f"Getting structure count...")
    structure_count = get_structure_count(tar_paths)
    chunk_count = int(np.ceil(structure_count / chunk_size))
    excluded_results = {}

    processes = os.cpu_count() - 1
    pool = Pool(processes=processes)
    func = partial(run_dssp_chunk, dssp_executable = dssp_executable, forbidden_codes = forbidden_codes,
                   plddt_thres = plddt_thres)

    with trange(chunk_count, desc = f"Running DSSP for chunks of structures in tar archive...") as pbar:
        for i, excluded_results_chunk in enumerate(pool.imap_unordered(func, stream_structures(tar_paths, chunk_size))):
            excluded_results = excluded_results | excluded_results_chunk
            pbar.update()

    return excluded_results

current_file_path = __file__
directory_path = os.path.dirname(os.path.abspath(current_file_path))
alphadssp_path = os.path.join(directory_path, "alphadssp_excluded_results.pkl")

def fuse_accession(args, stride = 200, trim_factor = 0.5):
    accession, entries = args

    # Find end residue
    ending_residues = []
    for base_name, (high_confidence_forbidden, _) in entries:
        model_number = int(base_name.split("-")[2][1:])
        starting_residue = stride * (model_number - 1) + 1
        entry_ending_residue = starting_residue + len(high_confidence_forbidden) - 1
        ending_residues.append(entry_ending_residue)
    end_res = max(ending_residues)

    # Iterate over fragments to combine
    total_high_confidence_forbidden = np.full(shape=end_res + 1, fill_value=True, dtype=bool)
    total_dssp_codes = np.full(shape=end_res + 1, fill_value="-", dtype="<U1")
    trim_amount = stride * trim_factor
    for base_name, (high_confidence_forbidden, dssp_codes_str) in entries:
        dssp_codes = np.array(list(dssp_codes_str))
        base_name_elements = base_name.split("-")
        model_number = int(base_name_elements[2][1:])
        hcf_len = len(high_confidence_forbidden)

        starting_idx = stride * (model_number - 1)
        ending_idx = starting_idx + hcf_len
        if starting_idx == 0:
            trimmed_starting_idx = starting_idx
            trimmed_ending_idx = ending_idx - trim_amount
            trimmed_hcf_mask = high_confidence_forbidden[:-trim_amount]
            trimmed_dssp_codes = dssp_codes[:-trim_amount]
        elif ending_idx == end_res:
            trimmed_starting_idx = starting_idx + trim_amount
            trimmed_ending_idx = ending_idx
            trimmed_hcf_mask = high_confidence_forbidden[trim_amount:]
            trimmed_dssp_codes = dssp_codes[trim_amount:]
        else:
            trimmed_starting_idx = starting_idx + trim_amount
            trimmed_ending_idx = ending_idx - trim_amount
            trimmed_hcf_mask = high_confidence_forbidden[trim_amount:-trim_amount]
            trimmed_dssp_codes = dssp_codes[trim_amount:-trim_amount]

        previous_total_hcf_snippet = total_high_confidence_forbidden[trimmed_starting_idx:trimmed_ending_idx]
        new_total_hcf_snippet = np.logical_and(trimmed_hcf_mask, previous_total_hcf_snippet)
        total_high_confidence_forbidden[trimmed_starting_idx:trimmed_ending_idx] = new_total_hcf_snippet
        total_dssp_codes[trimmed_starting_idx:trimmed_ending_idx] = trimmed_dssp_codes

    total_dssp_codes = "".join(total_dssp_codes)
    output = (accession, (total_high_confidence_forbidden, total_dssp_codes))

    return output

def categorize_keys(keys):
    unfragmented_keys = {}
    fragmented_keys = {}
    accessions = [key.split("-")[1] for key in keys]

    # Use a dictionary to count occurrences of each accession
    accession_count = {}
    for accession in accessions:
        if accession in accession_count:
            accession_count[accession] += 1
        else:
            accession_count[accession] = 1

    # Iterate over keys and accessions together
    for key, accession in zip(keys, accessions):
        count = accession_count[accession]
        if count == 1:
            unfragmented_keys[accession] = key
        else:
            if accession not in fragmented_keys:
                fragmented_keys[accession] = [key]
            else:
                fragmented_keys[accession].append(key)

    return unfragmented_keys, fragmented_keys

def parse_fragments(excluded_results, verbose = True):
    '''
    This function converts excluded_results to a dict of accession --> (high_confidence_forbidden, dssp_codes_str)
    It combines fragments when they exist for large proteins.

    Args:
        excluded_results (dict): output from run_dssp_parallel()
        stride (int):            amount that the frame moves for each consecutive overlapping fragment in large entries
        trim_factor (int):       fraction of the stride to trim off the ends, accounting for low certainty in termini

    Returns:
        accession_results (dict): dictionary of accession --> (high_confidence_forbidden, dssp_codes_str)
    '''

    print(f"Converting model dict (n={len(excluded_results)} models) into accession dict...") if verbose else None

    keys = list(excluded_results.keys())
    unfragmented_keys, fragmented_keys = categorize_keys(keys)

    accession_results = {} # final dict
    chunked_entries = {} # temporary dict for lists of overlapping models as (key, value) pairs

    # Collect results that represent entire accessions (i.e. unfragmented)
    for accession, key in unfragmented_keys.items():
        accession_results[accession] = excluded_results[key]

    # Collect fragmented results for large proteins with overlapping fragment models
    for accession, keys in fragmented_keys.items():
        for key in keys:
            value = excluded_results[key]
            if chunked_entries.get(accession) is None:
                chunked_entries[accession] = [(key, value)]
            else:
                chunked_entries[accession].append((key, value))

    # Handle accessions with overlapping fragment models
    if len(chunked_entries) > 0:
        pool = multiprocessing.Pool()
        with trange(len(chunked_entries), desc=f"Combining fragments for larger accessions...") as pbar:
            for accession, results in pool.imap(fuse_accession, chunked_entries.items()):
                accession_results[accession] = results
                pbar.update()
            pool.close()
            pool.join()
    else:
        max_hcf_len = max([value[0].shape[0] for value in accession_results.values()])
        print(f"Models were not fragmented; longest model was {max_hcf_len}")

    return accession_results

def generate_dssp(tar_dir = None, dssp_executable="/usr/bin/dssp", forbidden_codes = ("H","B","E","G","I","T"),
                  plddt_thres=70, use_cached=True):
    '''
    Main function to generate DSSP results and an exclusion mask based on confident forbidden codes

    Args:
        tar_dir (str|None):           AlphaFold tar shards directory; this can be obtained by running this command:
                                      `gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-[TAX ID]-*_v4.tar .`
        dssp_executable (str):        path to locally installed DSSP executable
        forbidden_codes (list|tuple): disallowed DSSP codes that will be used for generating the exclusion mask
        plddt_thres (int):            threshold for pLDDT such that only confident disallowed DSSP codes are used
        use_cached (bool):            whether to use cached (pickled) AlphaDSSP data; if no, it is rebuilt

    Returns:
        results (dict): dictionary of full entry name --> tuple of (high_confidence_forbidden, dssp_codes_str)
    '''

    if tar_dir is None:
        tar_dir = input("Enter the path to the folder containing tar shards of Alphafold structures:  ")

    # Reload from previous build if desired
    tar_folder_name = tar_dir.rsplit("/", 1)[1]
    pickled_name = f"alphadssp_excluded_results_{tar_folder_name}.pkl"
    alphadssp_path = os.path.join(directory_path, pickled_name)
    if os.path.exists(alphadssp_path):
        with open(alphadssp_path, "rb") as file:
            results = pickle.load(file)
            return results

    tar_paths = [os.path.join(tar_dir, filename) for filename in os.listdir(tar_dir)]
    results = run_dssp_parallel(tar_paths, dssp_executable, forbidden_codes, plddt_thres)
    results = parse_fragments(results)
    with open("../alphadssp_excluded_results.pkl", "wb") as file:
        pickle.dump(results, file)

    return results

if __name__ == "__main__":
    generate_dssp()