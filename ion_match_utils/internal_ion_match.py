from .ProteinClass import Protein,Clip,Ion,C_HMod,Mod
from .ion_match_utils import get_matched_index,construct_CM_series
import pandas as pd
from pyteomics import mass
#from .utils import *
def get_internal_CM_output(mono_mass_arr,protein,ion_type_list,ppm,unloc_mod_df):
    seqLen = protein.SEQLEN
    #保证即使没有匹配到离子仍然有输出。
    CM_output_template = pd.DataFrame(columns = range(10))
    #先匹配一遍不带非固定修饰的离子，再匹配非固定修饰的离子
    for start in range(2,seqLen):#内部离子不包含两端氨基酸。start=[2,seqLen-1]--zhuyl,230614
        #start += 1
        for end in range(start,seqLen):#不包含C-氨基酸。end=[start,seqLen-1]--zhuyl,230614
            #end += 1
            pep = Clip(protein).clip(start,end)
            for ion_type in ion_type_list:
                ion = Ion(pep).ionization(ion_type)
                #先将没有unloc_mod的离子搜索一遍
                matched_mass_index = get_matched_index(mono_mass_arr,ion,ppm)#考虑一个实验离子匹配到多个理论离子的情况
                matched_mass_df = mono_mass_arr[matched_mass_index]
                for _,matched_mass_series in matched_mass_df.iterrows():
                    CM_output_series = construct_CM_series(matched_mass_series,ion,start,end,ion_type,list(pep.mod_list.values()),[])
                    CM_output_template = CM_output_template.append(CM_output_series,ignore_index=True)
                #然后再搜索有unloc_mod的离子
                if unloc_mod_df is not None:
                    #is_added_mod = False#判断是否加入了unloc_mod
                    #添加可变修饰时记录修饰名字
                    unloc_mod_list = []
                    for _,unloc_mod_series in unloc_mod_df.iterrows():
                        name,formula,start_loc,end_loc,mod_ion_type = unloc_mod_series
                        #start_loc 或者end_loc是any，在ion的第一个氨基酸加上修饰
                        if (start_loc == "any" or end_loc == "any") and (ion_type == mod_ion_type or mod_ion_type == "any"):
                            unloc_mod_list.append(Mod(name = name,formula = formula,loc = 1,_mass = mass.calculate_mass(formula=formula)))
                        #只要离子有氨基酸在unloc_mod限定的范围内，就加上该修饰
                        elif (start >= start_loc and start <= end_loc) and (ion_type == mod_ion_type or mod_ion_type == "any"):
                            unloc_mod_list.append(Mod(name = name,formula = formula,loc = 1,_mass = mass.calculate_mass(formula=formula)))
                        elif (end >= start_loc and end <= end_loc) and (ion_type == mod_ion_type or mod_ion_type == "any"):
                            unloc_mod_list.append(Mod(name = name,formula = formula,loc = 1,_mass = mass.calculate_mass(formula=formula)))
                        else:
                            pass
                    if len(unloc_mod_list)>0:
                        for unloc_mod in unloc_mod_list:
                            #将unloc_mod顺序添加然后进行匹配--zhuyl,230228
                            modified_ion = ion + unloc_mod
                            matched_mass_index = get_matched_index(mono_mass_arr,modified_ion,ppm)#考虑一个实验离子匹配到多个理论离子的情况
                            matched_mass_df = mono_mass_arr[matched_mass_index]
                            for _,matched_mass_series in matched_mass_df.iterrows():
                            #matched_mass_series = get_matched_mass(mono_mass_arr,ion,ppm)
                            #print(matched_mass_series)
                                CM_output_series = construct_CM_series(matched_mass_series,modified_ion,start,end,ion_type,list(pep.mod_list.values()),[unloc_mod])
                                CM_output_template = CM_output_template.append(CM_output_series,ignore_index=True)
                    else:
                        pass
                else:
                    pass
    return CM_output_template