import json
import re
import glob
import sys
import os
import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PandaUV_core import Param

MOD_FORMULAS = {
    "Acetyl": "C2H2O",
}


# read psrm file from toppic1.5.4
def parse_prsm_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    json_str = content.replace("prsm_data =\n", "", 1)
    return json.loads(json_str)


# get pure sequence from annotated sequence
# not consider unknown mass shift yet
def extract_sequence(annotated_seq):
    match = re.search(r"\.(.+)\.", annotated_seq)
    if match:
        seq_with_mods = match.group(1)
        seq_clean = re.sub(r"\[[^\]]+\]", "", seq_with_mods)
        seq_clean = re.sub(r"[()]", "", seq_clean)
        return seq_clean
    return annotated_seq


# get fixed mod from annotated sequence
def extract_fixed_mod(annotated_seq):
    pattern = r"\(([A-Z])\)\[([^\]]+)\]"
    matches = re.findall(pattern, annotated_seq)
    if not matches:
        return []

    seq_between_dots = re.search(r"\.(.+)\.", annotated_seq)
    if not seq_between_dots:
        return []

    core_seq = seq_between_dots.group(1)
    fixed_mods = []

    for aa, mod_name in matches:
        pos_in_seq = core_seq.find(f"({aa})[{mod_name}]")
        if pos_in_seq != -1:
            loc = pos_in_seq + 1
            formula = MOD_FORMULAS.get(mod_name, "")
            fixed_mods.append([mod_name, formula, loc])

    return fixed_mods


def prsm_to_pandauv_param(prsm_data):
    header = prsm_data["prsm"]["ms"]["ms_header"]
    annotation = prsm_data["prsm"]["annotated_protein"]["annotation"]

    prsm_id = int(prsm_data["prsm"]["prsm_id"])
    scans = int(header["scans"])
    annotated_seq = annotation["annotated_seq"]

    sequence = extract_sequence(annotated_seq)
    fixed_mods = extract_fixed_mod(annotated_seq)

    return {
        "prsm_id": prsm_id,
        "scans": scans,
        "sequence": {str(scans): sequence},
        "fixed_mod": {"header": ["name", "formula", "loc"], str(scans): fixed_mods},
    }


# get pure sequence and mod and update to Panda-UV Param
def parse_prsm_directory(msalign_file_dir, mzml_file_dir, workplace_dir, prsm_dir):
    param = Param()
    base_param = Param().get_param_template()
    base_param["msalign_file_dir"] = msalign_file_dir
    base_param["mzml_file_dir"] = mzml_file_dir
    base_param["workplace_dir"] = workplace_dir

    print(f"Current working directory: {os.getcwd()}")
    print(f"Searching in: {prsm_dir}")
    print(f"Full search pattern: {os.path.join(prsm_dir, 'prsm*.js')}")

    prsm_files = sorted(glob.glob(os.path.join(prsm_dir, "prsm*.js")))
    print(f"Found {len(prsm_files)} prsm files: {prsm_files}")

    for file_path in tqdm.tqdm(prsm_files):
        prsm_data = parse_prsm_file(file_path)
        sub_param = prsm_to_pandauv_param(prsm_data)

        scans = sub_param["scans"]
        scan_key = str(scans)
        prsm_id = sub_param["prsm_id"]

        base_param["scans"].append(scans)
        base_param["prsm_id"][scan_key] = prsm_id
        base_param["sequence"][scan_key] = sub_param["sequence"][scan_key]

        if sub_param["fixed_mod"][scan_key]:
            base_param["fixed_mod"][scan_key] = sub_param["fixed_mod"][scan_key]

    base_param["scans"].sort()
    param.update(base_param)
    return param


if __name__ == "__main__":
    #base_dir = r".\examples\CPTAC_Intact_rep1_15Jan15_Bane_C2-14-08-02RZ"
    base_dir = r"Z:\I\EnvCNN_Publish_Data\Ovarian_Tumor_Data\raw"
    mzml_file_dir = os.path.join(
        base_dir, "CPTAC_Intact_rep1_15Jan15_Bane_C2-14-08-02RZ.mzML"
    )
    msalign_file_dir = os.path.join(
        base_dir, "CPTAC_Intact_rep1_15Jan15_Bane_C2-14-08-02RZ_ms2.msalign"
    )
    prsm_dir = os.path.join(
        base_dir,
        r"CPTAC_Intact_rep1_15Jan15_Bane_C2-14-08-02RZ_html\toppic_prsm_cutoff\data_js\prsms",
    )
    workplace_dir = prsm_dir
    param = parse_prsm_directory(
        msalign_file_dir, mzml_file_dir, workplace_dir, prsm_dir
    )
    param.save_param(workplace_dir)
