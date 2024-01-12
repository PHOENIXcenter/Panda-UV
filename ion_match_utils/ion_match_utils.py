###保存利用Protein类和mono_mass_arr进行离子匹配的基本函数
import pandas as pd
import numpy as np
from .ProteinClass import Clip,Ion
from .utils import mz_tolerance,mz_tolerance,cal_ppm

#计算和理论离子碎片匹配上的实验离子索引,返回索引
def get_matched_index(mono_mass_arr,ion,ppm):
    left,right = mz_tolerance(ion.MASS,ppm)
    matched_mass_index = (mono_mass_arr.iloc[:,0]<=right) & (mono_mass_arr.iloc[:,0]>=left)
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