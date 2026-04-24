###离子匹配函数 - 无Protein类设计
import os
import sys
import re
import pandas as pd
import numpy as np
from pyteomics import mass
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ion_match_utils.utils import mz_tolerance, cal_ppm
from Averagine.iso_util import mass_to_formula

_atom_pattern = r'([A-Z][a-z+]*)([+-]?\d+)?'
_unknown_mod_cache = {}

ION_TYPE_MODIFIERS = {
    "a":   {"formula": "H-2O-2C-1", "mass": -46.005479303259996},
    "b":   {"formula": "H-2O-1",   "mass": -18.0105646837},
    "c":   {"formula": "H1O-1N1",  "mass": -0.9840155826899988},
    "c.":  {"formula": "H-4O-1N-1", "mass": -34.02928875264},
    "x":   {"formula": "H-2O1C1",  "mass": 25.97926455542},
    "y":   {"formula": "",           "mass": 0},
    "z":   {"formula": "H-3N-1",   "mass": -17.02654910101},
    "-H":   {"formula": "H-1",      "mass": -1.00782503207},
    "H":    {"formula": "H",         "mass": 1.00782503207},
    "a+1":  {"formula": "H-1O-2C-1", "mass": -44.99765427119},
    "a-1":  {"formula": "H-3O-2C-1", "mass": -47.01330433533},
    "c-1":  {"formula": "O-1N1", "mass": -1.9918406147599988},
    "c+1":  {"formula": "H2O-1N1", "mass": 0.023809449380001624},
    "x+1":  {"formula": "H-1O1C1", "mass": 26.98708958749},
    "x-1":  {"formula": "H-3O1C1", "mass": 24.97143952335},
    "y-1":  {"formula": "H-1",       "mass": -1.00782503207},
    "y-2":  {"formula": "H-2",       "mass": -2.01565006414},
    "z+1":  {"formula": "H-2N-1",   "mass": -16.01872406894},
    "z-1":  {"formula": "H-4N-1", "mass": -18.03437413308},
    "ax":   {"formula": "H-2O-1", "mass": -18.0105646837},
    "ay":   {"formula": "H-2C1", "mass": 9.98434993586},
    "az":   {"formula": "H-3C1N1", "mass": 22.97959890859},
    "az+1": {"formula": "H-2C1N1", "mass": 23.98742394066},
    "az+2": {"formula": "H-1N1C1", "mass": 24.99524897273},
    "bx":   {"formula": "H-2O-2C-1", "mass": -46.005479303259996},
    "by":   {"formula": "H-2O-1",   "mass": -18.0105646837},
    "bz":   {"formula": "H-3O-1N1", "mass": -5.014490711909998},
    "bz+2": {"formula": "H-1O-1N1", "mass": -2.9996656468299986},
    "cx":   {"formula": "H-3N-1O-2C-1", "mass": -61.01657834013},
    "cy":   {"formula": "H-3N-1O-1", "mass": -33.021463720569996},
    "cz":   {"formula": "H-4O-1", "mass": -20.026214747839998},
    "cz+2": {"formula": "H-2O-1", "mass": -18.010564683699998},
}

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

def comp_to_formula(formula_dict):
    formula = ""
    for k,v in formula_dict.items():
        formula += str(k)+str(v)
    return formula

def formula_init(formula):
    tmp_dict = {}
    for elem, number in re.findall(_atom_pattern, formula):
        if elem in tmp_dict.keys():
            tmp_dict[elem] += int(number) if number else 1
        else:
            tmp_dict[elem] = int(number) if number else 1
    return comp_to_formula(tmp_dict)

def combine_formulas(*formulas):
    """合并多个分子式，返回合并后的字符串"""
    combined = ""
    for formula in formulas:
        if not formula:
            continue
        combined += formula
    if not combined:
        return ""
    combined = formula_init(combined)
    return combined


def _process_unknown_mod(name, formula):
    """处理未知修饰，返回 (final_formula, final_mass)

    如果name是纯数字且formula为unknown，用averagine推断分子式
    结果会被缓存以避免重复计算
    """
    cache_key = (name, formula)
    if cache_key in _unknown_mod_cache:
        return _unknown_mod_cache[cache_key]

    if name.replace('.', '', 1).isdigit() and formula.lower() == "unknown":
        inferred_formula = mass_to_formula(float(name))
        print(f"Warning: Unknown formula for modification {name}, inferred as {inferred_formula}")
        result = (inferred_formula, float(name))
    else:
        result = (formula, mass.calculate_mass(formula=formula))

    _unknown_mod_cache[cache_key] = result
    return result


def _get_applicable_fixed_mods(fixed_mod_df, start, end):
    """获取适用于当前肽段的固定修饰列表

    参数:
        fixed_mod_df: DataFrame with columns ["name", "formula", "loc"]
        start, end: 肽段位置 (1-indexed)

    返回:
        list of (mass, formula, name) tuples
    """
    if fixed_mod_df is None or fixed_mod_df.empty:
        return []

    applicable = []
    for _, row in fixed_mod_df.iterrows():
        mod_loc = row["loc"]
        if start <= mod_loc <= end:
            formula = row["formula"]
            name = row["name"]
            _, mod_mass = _process_unknown_mod(name, formula) if formula else (None, 0)
            applicable.append((mod_mass, formula, name))
    return applicable


def _get_applicable_unloc_mods(unloc_mod_df, ion_type, start, end):
    """获取适用于当前肽段的非固定修饰列表

    参数:
        unloc_mod_df: DataFrame with columns ["name", "formula", "start_loc", "end_loc", "mod_ion_type"]
        ion_type: 离子类型
        start, end: 肽段位置 (1-indexed)

    返回:
        list of (mass, formula, name) tuples
    """
    if unloc_mod_df is None or unloc_mod_df.empty:
        return []

    applicable = []
    for _, row in unloc_mod_df.iterrows():
        name = row["name"]
        formula = row["formula"]
        start_loc = row["start_loc"]
        end_loc = row["end_loc"]
        mod_ion_type = row["ion type"]

        if not (ion_type == mod_ion_type or mod_ion_type == "any"):
            continue

        if not (start_loc == "any" or end_loc == "any" or
                start_loc <= start <= end_loc or
                start_loc <= end <= end_loc):
            continue

        final_formula, final_mass = _process_unknown_mod(name, formula)
        applicable.append((final_mass, final_formula, name))

    return applicable


def calculate_ion(sequence, start, end, ion_type, fixed_mods, unloc_mods):
    """计算离子碎片的质量和分子式

    参数:
        sequence: 蛋白序列字符串
        start, end: 肽段位置 (1-indexed)
        ion_type: 离子类型如 "a", "b", "y"
        fixed_mods: list of (mass, formula, name) for fixed mods applicable to this peptide
        unloc_mods: list of (mass, formula, name) for unloc mods applicable to this peptide

    返回:
        dict with "mass", "formula", "sequence"
    """
    peptide_seq = sequence[start-1:end]

    base_mass = mass.fast_mass2(sequence=peptide_seq, charge=0)
    base_formula = comp_to_formula(mass.Composition(sequence=peptide_seq))

    ion_info = ION_TYPE_MODIFIERS[ion_type]
    total_mass = base_mass + ion_info["mass"]
    total_formula = combine_formulas(base_formula, ion_info["formula"])

    for mod_mass, mod_formula, _ in fixed_mods:
        total_mass += mod_mass
        total_formula = combine_formulas(total_formula, mod_formula)

    for mod_mass, mod_formula, _ in unloc_mods:
        total_mass += mod_mass
        total_formula = combine_formulas(total_formula, mod_formula)

    return {
        "mass": total_mass,
        "formula": total_formula,
        "sequence": peptide_seq
    }


def _match_ion(mono_mass_arr, ion_info, ion_type, start, end, fixed_mods, unloc_mods, ppm):
    """匹配单个离子类型的所有可能离子

    参数:
        mono_mass_arr: 实验离子数据 (N x 4 array: mass, intensity, charge, mz)
        ion_info: calculate_ion 返回的 dict
        ion_type: 离子类型
        start, end: 肽段位置
        fixed_mods: 固定修饰列表
        unloc_mods: 非固定修饰列表
        ppm: ppm tolerance

    返回:
        list of dict (匹配结果)
    """
    results = []
    ion_mass = ion_info["mass"]
    ion_formula = ion_info["formula"]
    peptide_seq = ion_info["sequence"]

    left, right = mz_tolerance(ion_mass, ppm)
    mask = (mono_mass_arr[:, 0] >= left) & (mono_mass_arr[:, 0] <= right)
    matched = mono_mass_arr[mask]

    fixed_mod_name = "|".join([m[2] for m in fixed_mods]) if fixed_mods else ""
    unloc_mod_name = "|".join([m[2] for m in unloc_mods]) if unloc_mods else ""

    for mass_series in matched:
        results.append({
            "Frag Type": ion_type,
            "Observed Mass": mass_series[0],
            "Theoretical Mass": ion_mass,
            "Start AA": start,
            "End AA": end,
            "Error": cal_ppm(mass_series[0], ion_mass),
            "Fixed Mod": fixed_mod_name if fixed_mod_name else 0,
            "Unlocalized Mod": unloc_mod_name if unloc_mod_name else 0,
            "Sequence": peptide_seq,
            "Intensity": mass_series[1],
            "Formula": ion_formula,
            "Charge": mass_series[2],
            "mz": mass_series[3],
        })

    return results


def _position_generator(mode, seqLen):
    if mode == "N":
        start = 1
        for end in range(1, seqLen):
            yield start, end
    elif mode == "C":
        end = seqLen
        for start in range(2, seqLen + 1):
            yield start, end
    elif mode == "internal":
        for start in range(2, seqLen):
            for end in range(start, seqLen):
                yield start, end


def get_ion_output(mono_mass_arr, sequence, fixed_mod_df, unloc_mod_df, ion_type_list, ppm, mode):
    all_results = []
    seqLen = len(sequence)

    for start, end in _position_generator(mode, seqLen):
        fixed_mods = _get_applicable_fixed_mods(fixed_mod_df, start, end)
        for ion_type in ion_type_list:
            unloc_mods = _get_applicable_unloc_mods(unloc_mod_df, ion_type, start, end)
            #if applicable unloc mod exists first match ion with unloc mod
            if len(unloc_mods):
                ion_info = calculate_ion(sequence, start, end, ion_type, fixed_mods, unloc_mods)
                results = _match_ion(mono_mass_arr, ion_info, ion_type, start, end, fixed_mods, unloc_mods, ppm)
                all_results.extend(results)
            #match ion without unloc mod anyway
            ion_info = calculate_ion(sequence, start, end, ion_type, fixed_mods, [])
            results = _match_ion(mono_mass_arr, ion_info, ion_type, start, end, fixed_mods, [], ppm)
            all_results.extend(results)
            
    if not all_results:
        return pd.DataFrame(columns=output_columns)
    return pd.DataFrame(all_results)

def get_all_output(
    mono_mass_arr,
    sequence,
    fixed_mod_df,
    unloc_mod_df,
    n_terminal_frag_type,
    c_terminal_frag_type,
    internal_frag_type,
    terminal_mass_error,
    internal_mass_error,
):
    """统一的离子匹配输出函数"""
    
    final_output = []

    if len(n_terminal_frag_type):
        N_Terminal_output = get_ion_output(
            mono_mass_arr,
            sequence,
            fixed_mod_df,
            unloc_mod_df,
            n_terminal_frag_type,
            terminal_mass_error,
            "N",
        )
        if len(N_Terminal_output):
            final_output.append(N_Terminal_output)

    if len(c_terminal_frag_type):
        C_Terminal_output = get_ion_output(
            mono_mass_arr,
            sequence,
            fixed_mod_df,
            unloc_mod_df,
            c_terminal_frag_type,
            terminal_mass_error,
            "C",
        )
        if len(C_Terminal_output):
            final_output.append(C_Terminal_output)

    if len(internal_frag_type):
        Internal_output = get_ion_output(
            mono_mass_arr,
            sequence,
            fixed_mod_df,
            unloc_mod_df,
            internal_frag_type,
            internal_mass_error,
            "internal",
        )
        if len(Internal_output):
            final_output.append(Internal_output)

    if len(final_output) == 0:
        return pd.DataFrame(columns=output_columns)

    final_output = pd.concat(final_output, ignore_index=True)
    return pd.DataFrame(final_output.values, columns=output_columns)

if __name__ == "__main__":
    test_formula = combine_formulas(comp_to_formula(mass.Composition(sequence="PEP")))
    print(test_formula)
    calculate_ion("MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG",1,5,"b",[],[])
    pass