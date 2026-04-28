"""
PRSM Parser Module

Parse PRSM (Proteomics Results Statistical Model) files from Toppic 1.5.4
and convert them to Panda-UV parameter format.

Main Functions:
    - parse_prsm_file: Read and parse single prsm*.js file
    - extract_sequence: Extract pure sequence from annotated sequence
    - extract_fixed_mod: Extract fixed modifications (single AA site)
    - extract_unloc_mod: Extract unlocalized modifications (multi-AA site or unknown)
    - prsm_to_pandauv_param: Convert prsm data to Panda-UV param dict
    - parse_prsm_directory: Batch process all prsm files in directory
"""

import json
import re
import glob
import os
import sys
import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PandaUV_core import Param

# Known modification formulas dictionary
# Key: modification name, Value: chemical formula
MOD_FORMULAS = {
    "Acetyl": "C2H2O",
    "Carbamidomethyl": "C2H5NO",
    "Carboxymethyl": "C2H2O2",
    "Phospho": "PO3H",
    "Oxidation": "O",
    "Methyl": "CH2",
    "Dimethyl": "C2H4",
    "Trimethyl": "C3H6",
    "Deamidated": "NH",
}


def parse_prsm_file(file_path):
    """Read and parse a single PRSM file from Toppic 1.5.4.

    Args:
        file_path: Path to prsm*.js file

    Returns:
        dict: Parsed JSON data from prsm file
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Remove "prsm_data =\n" prefix added by Toppic
    json_str = content.replace("prsm_data =\n", "", 1)
    return json.loads(json_str)


def extract_sequence(annotated_seq):
    """Extract pure sequence from annotated sequence by removing modifications.

    Args:
        annotated_seq: Annotated sequence, e.g. K.SYKMAD(E)[Acetyl]AGSEADHEK.R

    Returns:
        str: Pure sequence without modifications, e.g. SYKMADAGSEADHEK
    """
    # Extract sequence between dots (e.g. SYKMAD(E)[Acetyl]AGSEADHEK)
    match = re.search(r"\.(.+)\.", annotated_seq)
    if match:
        seq_with_mods = match.group(1)
        # Remove [modification] parts
        seq_clean = re.sub(r"\[[^\]]+\]", "", seq_with_mods)
        # Remove parentheses
        seq_clean = re.sub(r"[()]", "", seq_clean)
        return seq_clean
    return annotated_seq

def extract_mods(core_seq):
    i=0
    AA_num = 1
    fixed_mods = []
    unloc_mods = []
    while(i<len(core_seq)):
        if core_seq[i] == "(":
            i+=1
            start_loc = AA_num
            while(core_seq[i]!=")"):
                i+=1
                AA_num+=1
            AA_num-=1
            end_loc = AA_num
            mod_name = ""
            i+=1
            if core_seq[i]=="[":
                i+=1
                while(core_seq[i]!="]"):
                    mod_name+=core_seq[i]
                    i+=1
            else:
                assert False, f"Annotated sequence Error: {core_seq}"
            mod_formula = MOD_FORMULAS.get(mod_name,"unknown")
            if start_loc==end_loc:
                fixed_mods.append([mod_name,mod_formula,start_loc])
            else:
                unloc_mods.append([mod_name,mod_formula,start_loc,end_loc,"any"])
        else:
            i+=1
            AA_num+=1
    return (fixed_mods,unloc_mods)


def prsm_to_pandauv_param(prsm_data):
    """Convert prsm data to Panda-UV parameter format.

    Args:
        prsm_data: Parsed prsm JSON data

    Returns:
        dict: Parameter dict containing:
            - prsm_id: PRSM identification number
            - scans: Scan number
            - sequence: {scan: pure_sequence}
            - fixed_mod: {header: [...], scan: [[name, formula, loc], ...]}
            - unloc_mod: {header: [...], scan: [[name, formula, start_loc, end_loc, ion_type], ...]}
    """
    # Extract header and annotation from prsm data structure
    header = prsm_data["prsm"]["ms"]["ms_header"]
    annotation = prsm_data["prsm"]["annotated_protein"]["annotation"]

    # Get basic info
    prsm_id = int(prsm_data["prsm"]["prsm_id"])
    scans = int(header["scans"])
    annotated_seq = annotation["annotated_seq"]

    # Extract sequence and modifications
    sequence = extract_sequence(annotated_seq)

    seq_between_dots = re.search(r"\.(.+)\.", annotated_seq)
    core_seq = seq_between_dots.group(1)
    fixed_mods,unloc_mods = extract_mods(core_seq)

    sub_param = {
        "prsm_id": prsm_id,
        "scans": scans,
        "sequence": {str(scans): sequence},
        "fixed_mod": {"header": ["name", "formula", "loc"], str(scans): fixed_mods},
        "unloc_mod": {"header": ["name", "formula", "start_loc", "end_loc", "ion type"], str(scans): unloc_mods}
    }
    return sub_param


def parse_prsm_directory(msalign_file_dir, mzml_file_dir, workplace_dir, prsm_dir):
    """Batch process all prsm files in a directory and merge into Param object.

    Args:
        msalign_file_dir: Path to msalign file containing fragment ion data
        mzml_file_dir: Path to mzML file containing raw mass spectrum data
        workplace_dir: Working directory for output results
        prsm_dir: Directory containing prsm*.js files

    Returns:
        Param: Merged Param object with all prsm data
    """
    # Initialize Param with base template
    param = Param()
    base_param = Param().get_param_template()

    # Set file paths
    base_param["msalign_file_dir"] = msalign_file_dir
    base_param["mzml_file_dir"] = mzml_file_dir
    base_param["workplace_dir"] = workplace_dir

    print(f"Current working directory: {os.getcwd()}")
    print(f"Searching in: {prsm_dir}")
    print(f"Full search pattern: {os.path.join(prsm_dir, 'prsm*.js')}")

    # Find all prsm*.js files in directory
    prsm_files = sorted(glob.glob(os.path.join(prsm_dir, "prsm*.js")))
    print(f"Found {len(prsm_files)} prsm files: {prsm_files}")

    # Process each prsm file and merge into base_param
    for file_path in tqdm.tqdm(prsm_files):
        # Parse single prsm file
        prsm_data = parse_prsm_file(file_path)
        sub_param = prsm_to_pandauv_param(prsm_data)

        # Extract values with scan as key
        scans = sub_param["scans"]
        scan_key = str(scans)
        prsm_id = sub_param["prsm_id"]

        # Append to base_param
        base_param["scans"].append(scans)
        base_param["prsm_id"][scan_key] = prsm_id
        base_param["sequence"][scan_key] = sub_param["sequence"][scan_key]

        # Merge fixed modifications if present
        if sub_param["fixed_mod"][scan_key]:
            base_param["fixed_mod"][scan_key] = sub_param["fixed_mod"][scan_key]

        # Merge unlocalized modifications if present
        if sub_param["unloc_mod"][scan_key]:
            base_param["unloc_mod"][scan_key] = sub_param["unloc_mod"][scan_key]

    # Sort scans list and update param
    base_param["scans"].sort()
    param.update(base_param)
    return param


if __name__ == "__main__":
    # Example 1: Full directory parsing
    base_dir = r".\examples\20250120_C_2ug_SV2_HCD_30NCE_C18_1"
    mzml_file_dir = os.path.join(
        base_dir, "20250120_C_2ug_SV2_HCD_30NCE_C18_1.mzML"
    )
    msalign_file_dir = os.path.join(
        base_dir, "20250120_C_2ug_SV2_HCD_30NCE_C18_1_ms2.msalign"
    )
    prsm_dir = os.path.join(
        base_dir,
        r"20250120_C_2ug_SV2_HCD_30NCE_C18_1_html\toppic_prsm_cutoff\data_js\prsms",
    )
    workplace_dir = prsm_dir
    param = parse_prsm_directory(
        msalign_file_dir, mzml_file_dir, workplace_dir, prsm_dir
    )
    param.save_param()