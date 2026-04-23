###保存利用Protein类和mono_mass_arr进行离子匹配的基本函数
import os
import sys
import pandas as pd
import numpy as np
from .ProteinClass import Clip,Ion,C_HMod,Mod
from .utils import mz_tolerance,cal_ppm
from pyteomics import mass
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Averagine.iso_util import mass_to_formula

def _process_unknown_mod(name, formula):
    """处理未知修饰，返回 (final_formula, final_mass)

    如果name是纯数字且formula为unknown，用averagine推断分子式
    """
    if name.replace('.', '', 1).isdigit() and formula.lower() == "unknown":
        inferred_formula = mass_to_formula(float(name))
        print(f"Warning: Unknown formula for modification {name}, inferred as {inferred_formula}")
        return inferred_formula, float(name)
    else:
        return formula, mass.calculate_mass(formula=formula)

#计算和理论离子碎片匹配上的实验离子索引,返回索引
def get_matched_index(mono_mass_arr,ion,ppm):
    left,right = mz_tolerance(ion.MASS,ppm)
    matched_mass_index = (mono_mass_arr[:,0]<=right) & (mono_mass_arr[:,0]>=left)
    return matched_mass_index

#计算和理论离子质量最近的匹配上的实验离子
def get_closest_mass(mass_df,ion):
    ppm_arr = abs(cal_ppm(mass_df.iloc[:,0],ion.MASS))#注意一定要用绝对值
    return mass_df.iloc[np.argmin(ppm_arr),:]

#返回在一定ppm匹配上的实验离子series，如果匹配上了多个实验离子，则只取最近的离子。没有匹配上则返回empty df
def get_matched_mass(mono_mass_arr,ion,ppm,ppm_shift):
    matched_mass_index = get_matched_index(mono_mass_arr,ion,ppm,ppm_shift)
    matched_mass_df = mono_mass_arr[matched_mass_index]
    if matched_mass_df.empty:
        return matched_mass_df
    else:
        return get_closest_mass(matched_mass_df,ion)
    
#获取蛋白的离子碎片，可以选择加不加H+
def get_protein_ion(protein,start,end,ion_type,mode="M+H"):
    if mode=="M+H":
        return Ion(Clip(protein).clip(start,end)).ionization(ion_type)+C_HMod()
    else:
        return Ion(Clip(protein).clip(start,end)).ionization(ion_type)

#从mod_list返回name。但是从pep还原的mod_list是嵌套结构，需要比unloc_mod多一个循环
def get_fixed_mod_list_name(mod_list):
    mod_name_list = []
    for mods in mod_list:
        for mod in mods:
            mod_name_list.append(mod.name)
    mod_name = "|".join(mod_name_list)
    return mod_name

#从mod_list返回name
def get_unloc_mod_list_name(mod_list):
    mod_name_list = []
    for mod in mod_list:
        mod_name_list.append(mod.name)
    mod_name = "|".join(mod_name_list)
    return mod_name

#输入匹配上的mono_mass_arr_i和蛋白质离子等信息，输出UE_output_i
def construct_CM_series(mass_series,protein,start,end,ion_type,fixed_mod_list,unloc_mod_list):
    frag_type = ion_type
    observed_mass = mass_series[0]
    theoritical_mass = protein.MASS
    Start_AA = start
    End_AA = end
    Error = cal_ppm(observed_mass,theoritical_mass)
    Sequence = protein.seq
    Intensity = mass_series[1]
    Formula = protein.FORMULA
    Charge = mass_series[2]
    mz = mass_series[3]
    
    fixed_mod_name = get_fixed_mod_list_name(fixed_mod_list)
    #值为''时Pandas会保存为NaN，导致不能计算重复
    if fixed_mod_name is '':
        fixed_mod_name = 0
    nuloc_mod_name = get_unloc_mod_list_name(unloc_mod_list)
    if nuloc_mod_name is '':
        nuloc_mod_name = 0
    return pd.Series([frag_type,observed_mass,theoritical_mass,Start_AA,End_AA,Error,fixed_mod_name,nuloc_mod_name,Sequence,Intensity,Formula,Charge,mz])

def _get_unloc_mod_list(unloc_mod_df, ion_type, start, end):
    """构建适用于当前肽段的 unloc_mod 列表"""
    if unloc_mod_df is None:
        return []

    unloc_mod_list = []
    for _, unloc_mod_series in unloc_mod_df.iterrows():
        name, formula, start_loc, end_loc, mod_ion_type = unloc_mod_series

        if not (ion_type == mod_ion_type or mod_ion_type == "any"):
            continue

        if not (start_loc == "any" or end_loc == "any" or
                start_loc <= start <= end_loc or
                start_loc <= end <= end_loc):
            continue

        _mod_formula, _mod_mass = _process_unknown_mod(name, formula)
        unloc_mod_list.append(Mod(name=name, formula=_mod_formula, loc=1, _mass=_mod_mass))

    return unloc_mod_list

def _get_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df, mode, columns):
    """
    统一的离子匹配输出函数
    mode: "N" | "C" | "internal"
    columns: DataFrame 列数（12 for N-terminal, 10 for others）
    """
    seqLen = protein.SEQLEN
    CM_output_template = pd.DataFrame(columns=range(columns))

    def match_peptide(start, end, pep):
        for ion_type in ion_type_list:
            ion = Ion(pep).ionization(ion_type)
            matched_mass_index = get_matched_index(mono_mass_arr, ion, ppm)
            matched_mass_df = mono_mass_arr[matched_mass_index]
            for matched_mass_series in matched_mass_df:
                CM_output_series = construct_CM_series(matched_mass_series, ion, start, end, ion_type, list(pep.mod_list.values()), [])
                CM_output_template.loc[len(CM_output_template)] = CM_output_series

            unloc_mod_list = _get_unloc_mod_list(unloc_mod_df, ion_type, start, end)
            if len(unloc_mod_list) > 0:
                for unloc_mod in unloc_mod_list:
                    modified_ion = ion + unloc_mod
                    matched_mass_index = get_matched_index(mono_mass_arr, modified_ion, ppm)
                    matched_mass_df = mono_mass_arr[matched_mass_index]
                    for matched_mass_series in matched_mass_df:
                        CM_output_series = construct_CM_series(matched_mass_series, modified_ion, start, end, ion_type, list(pep.mod_list.values()), [unloc_mod])
                        CM_output_template.loc[len(CM_output_template)] = CM_output_series

    if mode == "N":
        start = 1
        for end in range(1, seqLen):
            pep = Clip(protein).clip(start, end)
            match_peptide(start, end, pep)
    elif mode == "C":
        end = seqLen
        for start in range(2, seqLen + 1):
            pep = Clip(protein).clip(start, end)
            match_peptide(start, end, pep)
    else:
        for start in range(2, seqLen):
            for end in range(start, seqLen):
                pep = Clip(protein).clip(start, end)
                match_peptide(start, end, pep)

    return CM_output_template

def get_Nterminal_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    return _get_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df, mode="N", columns=13)

def get_Cterminal_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    return _get_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df, mode="C", columns=13)

def get_internal_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df):
    return _get_output(mono_mass_arr, protein, ion_type_list, ppm, unloc_mod_df, mode="internal", columns=13)