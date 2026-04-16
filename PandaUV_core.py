from pyteomics import mass, mzml
import copy
import pandas as pd
import numpy as np
import json
from ion_match_utils.terminal_ion_match import (
    get_Nterminal_CM_output,
    get_Cterminal_CM_output,
)
from ion_match_utils.internal_ion_match import get_internal_CM_output
from ion_match_utils.ProteinClass import Protein, Mod
from ion_match_utils.utils import cal_mz
from MS_calibration.Scoring_function_utils import get_score_term
import argparse
import datetime
import os
import threading

H_proton_mass = 1.00782503207

from post_process_utils.post_process import get_process_info
from post_process_utils import stratage_4
from visual_utils.site_map_plot import seg_map_plot_main
from visual_utils.fragment_yeild_plot import fragment_abundance_plot_main
from msalign_utils.msalign_reader import get_dec_info


r_script = """
library(enviPat)
library(data.table)

FragIon.IsoPattern <- function(FragIons.chemform, ChargeZ){
  data(isotopes)
  Final.chemform <- paste0(FragIons.chemform, paste0('H', ChargeZ))
  CalPeaks <- isopattern(isotopes,
                         chemforms = Final.chemform,
                         charge = ChargeZ,
                         plotit = FALSE,
                         algo = 2,
                         emass = 0.00054858,
                         threshold=0.1,
                         verbose = FALSE)
  Cal.envelope <- envelope(CalPeaks,
                           verbose = FALSE,
                           resolution = 1E5,
                           dmz = 0.01)
  Cal.mz <- vdetect(Cal.envelope, detect="centroid", plotit= FALSE, verbose=FALSE)
  Cal.mz <- as.data.table(Cal.mz[[1]])
  return(Cal.mz)
}
"""


def print_time():
    t = datetime.datetime.now()
    print(t.strftime("%Y-%m-%d %H:%M:%S"))


def mono_preprocess(mono_mass_arr, ppm_shift):
    mono_mass_arr = copy.deepcopy(mono_mass_arr)
    mono_mass_arr[:, 0] = cal_mz(mono_mass_arr[:, 0], ppm_shift)
    return mono_mass_arr


def get_all_output(
    mono_mass_arr,
    protein,
    n_terminal_frag_type,
    c_terminal_frag_type,
    internal_frag_type,
    terminal_mass_error,
    internal_mass_error,
    unloc_mod_df,
):
    output_columns = [
        "Frag Type",
        "Observed Mass",
        "Theoretical Mass",
        "Start AA",
        "End AA",
        "Error",
        "Fixed Mod",
        "Unlocalized Mod",
        "Sequence",
        "Intensity",
        "Formula",
        "Charge",
        "mz",
    ]
    final_output = []
    internal_frag_type_len = len(internal_frag_type)
    n_terminal_frag_type_len = len(n_terminal_frag_type)
    c_terminal_frag_type_len = len(c_terminal_frag_type)
    if n_terminal_frag_type_len != 0:
        N_Terminal_output = get_Nterminal_CM_output(
            mono_mass_arr,
            protein,
            n_terminal_frag_type,
            terminal_mass_error,
            unloc_mod_df,
        )
        if len(N_Terminal_output):
            final_output.append(N_Terminal_output)
    if c_terminal_frag_type_len != 0:
        C_Terminal_output = get_Cterminal_CM_output(
            mono_mass_arr,
            protein,
            c_terminal_frag_type,
            terminal_mass_error,
            unloc_mod_df,
        )
        if len(C_Terminal_output):
            final_output.append(C_Terminal_output)
    if internal_frag_type_len != 0:
        Internal_output = get_internal_CM_output(
            mono_mass_arr,
            protein,
            internal_frag_type,
            internal_mass_error,
            unloc_mod_df,
        )
        if len(Internal_output):
            final_output.append(Internal_output)
    if len(final_output) == 0:
        return final_output
    final_output = pd.concat(final_output, ignore_index=True)
    final_output = pd.DataFrame(final_output.values, columns=output_columns)
    return final_output


def get_terminal_output(
    mono_mass_arr,
    protein,
    n_terminal_frag_type,
    c_terminal_frag_type,
    terminal_mass_error,
    unloc_mod_df,
):
    output_columns = [
        "Frag Type",
        "Observed Mass",
        "Theoretical Mass",
        "Start AA",
        "End AA",
        "Error",
        "Fixed Mod",
        "Unlocalized Mod",
        "Sequence",
        "Intensity",
        "Formula",
        "Charge",
        "mz",
    ]
    final_output = []
    n_terminal_frag_type_len = len(n_terminal_frag_type)
    c_terminal_frag_type_len = len(c_terminal_frag_type)
    if n_terminal_frag_type_len != 0:
        N_Terminal_output = get_Nterminal_CM_output(
            mono_mass_arr,
            protein,
            n_terminal_frag_type,
            terminal_mass_error,
            unloc_mod_df,
        )
        if len(N_Terminal_output):
            final_output.append(N_Terminal_output)
    if c_terminal_frag_type_len != 0:
        C_Terminal_output = get_Cterminal_CM_output(
            mono_mass_arr,
            protein,
            c_terminal_frag_type,
            terminal_mass_error,
            unloc_mod_df,
        )
        if len(C_Terminal_output):
            final_output.append(C_Terminal_output)
    if len(final_output) == 0:
        return final_output
    final_output = pd.concat(final_output, ignore_index=True)
    final_output = pd.DataFrame(final_output.values, columns=output_columns)
    return final_output


def get_terminal_error(terminal_output):
    return np.mean(terminal_output["Error"])


def add_mod(protein, mod_df):
    if mod_df is not None:
        print("Adding fixed mod...")
        for _, item in mod_df.iterrows():
            mod = Mod(
                name=item["name"],
                formula=item["formula"],
                loc=item["loc"],
                _mass=mass.calculate_mass(formula=item["formula"]),
            )
            protein += mod
    return protein


class Param(dict):
    def __init__(self):
        super().__init__()
        self.default_output_dir = "."
        self.default_filename = "Panda-UV_param.json"
        self.update(self.get_param_template())

    def get_param_template(self):
        """
        sequence: Dict, key is scan (str), value is protein sequence
                Example: {"3871": "MQIFVKTLTGKTITLEVEPSDTIENV...", "3876": "SGRGK..."}

        msalign_file_dir: Path to msalign file (contains fragment ion mass, charge, etc.)
                        File format: SCANS, MONO_MZ, MONO_MASS, CHARGE, INTENSITY

        mzml_file_dir: Path to mzML file (contains raw mass spectrum peak data)
                    Used for obtaining m/z and intensity during peak matching

        workplace_dir: Working directory path, output results will be saved here
                    Subdirectories named by prsm_id, e.g., workplace_dir/prsm346/

        r_env_dir: R environment directory path, used by enviPat library for isotope peak calculation

        unloc_mod: Variable modification config (header + scan indexed data)
                header: ["name", "formula", "start_loc", "end_loc", "ion type"]
                - name: modification name
                - formula: chemical formula of the modification
                - start_loc/end_loc: int or "any", modification position range, "any" means any position
                - ion type: ion type generated by the modification
                Example: {"header": [...], "3876": [["heme", "C34H31O4Fe", "any", "any", "any"]]}

        fixed_mod: Fixed modification config (header + scan indexed data)
                header: ["name", "formula", "loc"]
                - name: modification name
                - formula: chemical formula of the modification
                - loc: int, modification position
                Example: {"header": [...], "3876": [["Acetyl", "C2H2O", 1]]}

        mass_calibration: Whether to perform mass calibration (on deconvoluted fragment ions)

        ms_calibration: Whether to perform spectrum calibration (on raw peaks)

        mass_mode: Mass mode, "M" for monoisotopic mass, "MH" for protonated ion

        terminal_mass_error: Terminal ion (N-terminal/C-terminal) mass error threshold in ppm
                            Used in second_match for terminal ion matching

        internal_mass_error: Internal ion mass error threshold in ppm
                            Used in second_match for internal ion matching

        peak_match_error: Peak matching error threshold in ppm
                        Used in calculate_scores for PCC calculation

        n_terminal_frag_type: N-terminal ion fragment type list (e.g., a, b, c)

        c_terminal_frag_type: C-terminal ion fragment type list (e.g., x, y, z)

        internal_frag_type: Internal ion fragment type list (e.g., by)

        scans: List of scan to process (integer array)
            Example: [3871, 3876, 3877]

        prsm_id: Dict, key is scan (str), value is prsm_id (integer)
                Used to determine output directory name
                Example: {"3871": 346, "3876": 347}
                Output directories: workplace_dir/prsm346/, workplace_dir/prsm347/

        Returns:
            dict: A dictionary containing all default parameters
        """
        return {
            "sequence": {},
            "msalign_file_dir": "",
            "r_env_dir": "G:\\software\\R\\R-4.2.3",
            "unloc_mod": {
                "header": ["name", "formula", "start_loc", "end_loc", "ion type"]
            },
            "fixed_mod": {"header": ["name", "formula", "loc"]},
            "mass_calibration": False,
            "ms_calibration": False,
            "mass_mode": "M",
            "terminal_mass_error": 10,
            "internal_mass_error": 10,
            "peak_match_error": 10,
            "n_terminal_frag_type": ["b"],
            "c_terminal_frag_type": ["y"],
            "internal_frag_type": ["by"],
            "mzml_file_dir": "",
            "scans": [],
            "prsm_id": {},
            "workplace_dir": "",
            "thread": 4,
        }

    def save_param(self, param_output_dir=None):
        if param_output_dir is None:
            param_output_dir = os.path.join(
                self.default_output_dir, self.default_filename
            )
        else:
            param_output_dir = os.path.join(param_output_dir, self.default_filename)
        with open(param_output_dir, "w", encoding="utf-8") as f:
            json.dump(dict(self), f, indent=2, ensure_ascii=False)

    def read_param(self, param_input_dir=None):
        if param_input_dir is None:
            param_input_dir = os.path.join(
                self.default_output_dir, self.default_filename
            )
        if os.path.isfile(param_input_dir):
            with open(param_input_dir, "r", encoding="utf-8") as f:
                self.update(json.load(f))


class PandaUV:
    def __init__(self, param):
        self.param = param
        self.dec_info_list = None
        self.mzmlReader = None
        self.r_initialized = False
        self.r_source = None
        self.r_lock = None
        self.first_mass_match_ppm = 20
        if self.param["mass_mode"] == "M":
            self.add_H = False
        elif self.param["mass_mode"] == "MH+":
            self.add_H = True
        else:
            raise ValueError(f"Invalid mass_mode: {self.param['mass_mode']}")

    def _init_r_environment(self):
        os.environ["LC_ALL"] = "Chinese_China.65001"
        os.environ["R_HOME"] = self.param["r_env_dir"]
        import rpy2.robjects as robjects

        self.r_source = robjects.r
        self.r_source(r_script)
        self.r_initialized = True
        self.r_lock = threading.Lock()
        print(f"Initiating R environment: {os.environ['R_HOME']}")

    def _apply_mass_mode_adjustment(self, mono_arr):
        if self.add_H:
            mono_arr[:, 0] -= H_proton_mass
        return mono_arr

    def _add_mz_to_mono_arr(self, mono_arr):
        mz_arr = mono_arr[:, 0] / mono_arr[:, 2] + H_proton_mass
        mono_arr = np.hstack([mono_arr, mz_arr[:, np.newaxis]])
        return mono_arr

    def _get_mono_arr_by_scan(self, scan):
        for dec_info in self.dec_info_list:
            if scan == int(dec_info["SCANS"]):
                return dec_info["mono_arr"]
        return None

    def _get_mz_int_arr_by_scan(self, scan):
        for mzml_i in self.mzmlReader:
            if scan == int(mzml_i["index"]) + 1:
                mz_arr = mzml_i["m/z array"]
                int_arr = mzml_i["intensity array"]
                return np.stack([mz_arr, int_arr], axis=1)
        mzml_file_dir = self.param["mzml_file_dir"]
        assert False, f"No scans {scan} in file: {mzml_file_dir}"

    # init dec info list and mzmlReader, r env.
    def initialize(self):
        print_time()
        self.dec_info_list = get_dec_info(self.param["msalign_file_dir"])
        self.mzmlReader = list(mzml.read(self.param["mzml_file_dir"], use_index=True))
        self._init_r_environment()

    def get_unloc_mod(self, scan):
        unloc_mod_json = self.param.get("unloc_mod", "")
        if not unloc_mod_json or not isinstance(unloc_mod_json, dict):
            return None
        scan_key = str(scan)
        if scan_key not in unloc_mod_json:
            return None
        header = unloc_mod_json["header"]
        data = unloc_mod_json[scan_key]
        unloc_mod_df = pd.DataFrame(data, columns=header)
        if "start_loc" in unloc_mod_df.columns:
            unloc_mod_df["start_loc"] = unloc_mod_df["start_loc"].apply(
                lambda x: int(x) if x != "any" else x
            )
        if "end_loc" in unloc_mod_df.columns:
            unloc_mod_df["end_loc"] = unloc_mod_df["end_loc"].apply(
                lambda x: int(x) if x != "any" else x
            )
        return unloc_mod_df

    def get_fixed_mod(self, scan):
        fixed_mod_json = self.param.get("fixed_mod", "")
        if not fixed_mod_json or not isinstance(fixed_mod_json, dict):
            return None
        scan_key = str(scan)
        if scan_key not in fixed_mod_json:
            return None
        header = fixed_mod_json["header"]
        data = fixed_mod_json[scan_key]
        fixed_mod_df = pd.DataFrame(data, columns=header)
        if "loc" in fixed_mod_df.columns:
            fixed_mod_df["loc"] = fixed_mod_df["loc"].astype(int)
        return fixed_mod_df

    def load_protein(self, sequence):
        protein = Protein(sequence)
        print("Sequence: ", protein)
        print("Length: ", protein.SEQLEN)
        print("Mass: ", protein.MASS)
        return protein

    # first match get mass shift
    def first_match(self, mono_arr, protein, unloc_mod_df):
        mass_shift_ppm = 0
        n_terminal_frag_type = self.param["n_terminal_frag_type"]
        c_terminal_frag_type = self.param["c_terminal_frag_type"]

        mass_calibration = self.param["mass_calibration"]
        ms_calibration = self.param["ms_calibration"]

        if (mass_calibration or ms_calibration) and (
            len(n_terminal_frag_type) > 0 or len(c_terminal_frag_type) > 0
        ):
            terminal_output = get_terminal_output(
                mono_arr,
                protein,
                n_terminal_frag_type,
                c_terminal_frag_type,
                self.first_mass_match_ppm,
                unloc_mod_df,
            )
            if len(terminal_output) == 0:
                print("No fragment matched, please check input")
            else:
                mass_shift_ppm = get_terminal_error(terminal_output)
                print(f"Mass shift of terminal fragments: {mass_shift_ppm}")
        return mass_shift_ppm

    # calibrate mono mass and peak mz
    def calibrate_mass(self, mono_arr, mass_shift_ppm):
        mass_calibration = self.param["mass_calibration"]
        if mass_calibration:
            mono_arr[:, 0] = cal_mz(mono_arr[:, 0], mass_shift_ppm)
            print(f"Mass shift of deconvoluted fragments: {mass_shift_ppm} ppm")
        else:
            print(f"Mass shift of deconvoluted fragments: 0 ppm")
        return mono_arr

    def calibrate_mz(self, mz_int_arr, mass_shift_ppm):
        ms_calibration = self.param["ms_calibration"]
        if ms_calibration:
            mz_int_arr[:, 0] = cal_mz(mz_int_arr[:, 0], mass_shift_ppm)
            print(f"Spectral shift: {mass_shift_ppm} ppm")
        else:
            print(f"Spectral shift: 0 ppm")
        return mz_int_arr

    # second match get the terminal and internal fragment results
    def second_match(self, mono_arr, protein, unloc_mod_df):
        print("Matching fragments...")
        pandauv_output = get_all_output(
            mono_arr,
            protein,
            self.param["n_terminal_frag_type"],
            self.param["c_terminal_frag_type"],
            self.param["internal_frag_type"],
            self.param["terminal_mass_error"],
            self.param["internal_mass_error"],
            unloc_mod_df,
        )
        return pandauv_output

    # add PCC score to every matched fragments
    def calculate_scores(self, pandauv_output, mz_int_arr):
        print("PCC scoring...")

        def _get_score_with_lock(x):
            with self.r_lock:
                return get_score_term(
                    mz_int_arr, x, self.r_source, self.param["peak_match_error"]
                )

        score_term_series = pandauv_output.apply(_get_score_with_lock, axis=1)
        score_term_df = pd.DataFrame(
            np.vstack(score_term_series),
            columns=["PCC", "adjust_PCC", "dx", "dy", "peak num", "missing peak num"],
        )
        pandauv_output_with_PCC = pd.concat([pandauv_output, score_term_df], axis=1)
        return pandauv_output_with_PCC

    # drop the duplicated matches
    def post_process(self, protein, pandauv_output_with_PCC):
        print("Dropping duplicates...")
        seqLen = protein.SEQLEN
        pandauv_output_with_PCC = stratage_4.post_process(
            pandauv_output_with_PCC, seqLen
        )
        return pandauv_output_with_PCC

    def mk_output_dir(self, workplace_dir, prsm_id):
        output_dir = os.path.join(workplace_dir, f"prsm{prsm_id}")
        if os.path.exists(output_dir):
            pass
        else:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Make dirs: {output_dir}")
        return output_dir

    def _save_mono_arr(self, mono_arr, output_dir):
        output_filename = "mono_mass_with_charge.csv"
        pd.DataFrame(mono_arr).to_csv(
            os.path.join(output_dir, output_filename), index=False
        )
        print("DataFrame saving successful. ")

    def save_and_plot(
        self, protein, pandauv_output_with_PCC, mono_arr, sequence, output_dir
    ):

        print("Saving result....")
        pandauv_output_with_PCC.to_csv(
            f"{output_dir}/fragment_matching_result.csv", index=False
        )

        with open(f"{output_dir}/fragment_matching_result_sta.txt", mode="w") as f:
            f.write(get_process_info(pandauv_output_with_PCC, mono_arr, protein.SEQLEN))

        print(f"Output dir: {output_dir}")
        print_time()

        print("Plotting sequence cleavage maps....")
        seg_map_plot_main(output_dir, pandauv_output_with_PCC, sequence)

        """print("Plotting bar plots of residual fragment yield....")
        fragment_abundance_plot_main(output_dir, pandauv_output_with_PCC, sequence)"""
        print("Done.")

    def match(self, scan, sequence, workplace_dir):
        prsm_id = self.param["prsm_id"][str(scan)]
        output_dir = self.mk_output_dir(workplace_dir, prsm_id)
        mono_arr = self._get_mono_arr_by_scan(scan)
        mono_arr = self._apply_mass_mode_adjustment(mono_arr)
        mono_arr = self._add_mz_to_mono_arr(mono_arr)
        self._save_mono_arr(mono_arr, output_dir)
        mz_int_arr = self._get_mz_int_arr_by_scan(scan)
        unloc_mod_df = self.get_unloc_mod(scan)
        fixed_mod_df = self.get_fixed_mod(scan)
        protein = self.load_protein(sequence)
        protein = add_mod(protein, fixed_mod_df)
        mass_shift_ppm = self.first_match(mono_arr, protein, unloc_mod_df)
        mono_arr = self.calibrate_mass(mono_arr, mass_shift_ppm)
        mz_int_arr = self.calibrate_mz(mz_int_arr, mass_shift_ppm)
        pandauv_output = self.second_match(mono_arr, protein, unloc_mod_df)
        if len(pandauv_output) == 0:
            print(f"Scan {scan} not match fragments")
            return
        pandauv_output_with_PCC = self.calculate_scores(pandauv_output, mz_int_arr)
        pandauv_output_with_PCC = self.post_process(protein, pandauv_output_with_PCC)
        self.save_and_plot(
            protein, pandauv_output_with_PCC, mono_arr, sequence, output_dir
        )
        # return pandauv_output_with_PCC

    def run(self):
        self.initialize()
        for scan in self.param["scans"]:
            sequence = self.param["sequence"][str(scan)]
            print(f"Processing scan {scan}")
            self.match(scan, sequence, self.param["workplace_dir"])

    def run_parallel(self, max_workers=4):
        self.initialize()

        from concurrent.futures import ThreadPoolExecutor, as_completed

        scans = self.param["scans"]
        total_count = len(scans)
        completed_count = 0
        lock = threading.Lock()

        def process_one_scan(scan):
            nonlocal completed_count
            try:
                sequence = self.param["sequence"][str(scan)]
                print(f"Processing scan {scan}")
                self.match(scan, sequence, self.param["workplace_dir"])

                with lock:
                    completed_count += 1
                    print(f"Progress: {completed_count}/{total_count}")
            except Exception as e:
                with lock:
                    print(f"Scan {scan} failed with error: {e}")
                executor.shutdown(wait=False, cancel_futures=True)
                raise

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_one_scan, scan): scan for scan in scans}
            for future in as_completed(futures):
                scan = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Scan {scan} failed with error, stopping...")
                    executor.shutdown(wait=False, cancel_futures=True)
                    return


def main(param):
    panda_uv = PandaUV(param)
    thread_count = param.get("thread", 1)
    if thread_count > 1:
        panda_uv.run_parallel(max_workers=thread_count)
    else:
        panda_uv.run()


def argp():
    parser = argparse.ArgumentParser(
        prog="Panda-UV",
        description="An efficient tool for high confident fragment assignment of UVPD data",
    )
    parser.add_argument(
        "-param_dir", help="输入参数文件的路径", type=str, required=True
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    param = Param()
    param.read_param(
        r"Z:\I\EnvCNN_Publish_Data\Ovarian_Tumor_Data\raw\CPTAC_Intact_rep2_15Jan15_Bane_C2-14-08-02RZ_html\toppic_prsm_cutoff\data_js\prsms\Panda-UV_param.json"
    )
    # param.read_param("example_param.json")
    main(param)
