#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyteomics import mass,mzml

import copy

import re

import pandas as pd
import numpy as np

from ion_match_utils.terminal_ion_match import get_Nterminal_CM_output,get_Cterminal_CM_output

from ion_match_utils.internal_ion_match import get_internal_CM_output

from ion_match_utils.ProteinClass import NTermMod,Protein,Mod,Ion,Clip,N_HMod

from ion_match_utils.utils import cal_mz,cal_ppm

from MS_calibration.Scoring_function_utils import mz_shift,get_score_term,get_ms_peak_arr

import time

import argparse

import yaml

from post_process_utils.post_process import get_process_info
from post_process_utils import stratage_4

from visual_utils.site_map_plot import seg_map_plot_main
from visual_utils.fragment_yeild_plot import fragment_abundance_plot_main


# In[2]:


import datetime


# In[3]:


import sys
import os


# In[4]:


import yaml


# In[5]:


r_script = '''
library(enviPat)
library(data.table)

FragIon.IsoPattern <- function(FragIons.chemform, ChargeZ){
  # library(enviPat)
  # library(data.table)
  data(isotopes)
  #charge=1时，会添加H0，导致解析错误
  #if (ChargeZ==1){
  #  Final.chemform <- FragIons.chemform
  #}
  #else{
  #  Final.chemform <- paste0(FragIons.chemform, paste0('H', ChargeZ-1))#输入M+H的分子式，因此需要少加一个H--zhuyl 230410
  #}
  Final.chemform <- paste0(FragIons.chemform, paste0('H', ChargeZ))#改为默认输入M的分子式，不需要加H--zhuyl,230525
  CalPeaks <- isopattern(isotopes ,
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
  Cal.mz <- vdetect(Cal.envelope,detect="centroid",plotit= FALSE,verbose=FALSE)
  Cal.mz <- as.data.table(Cal.mz[[1]])
  return(Cal.mz)
}
'''


# In[6]:


def argp():
    paser=argparse.ArgumentParser(prog="PANDA-UV 2.0",
                                  description="An efficient tool for high confident fragment assignment of UVPD data")

    paser.add_argument('-param_dir', help='输入参数文件的路径', type=str, required=True)
    #paser.add_argument('-fixed_mod_dir', help='蛋白的修饰文件路径', type=str, required=False)
    args = paser.parse_args()
    return args


# In[7]:


def print_time():
    t = datetime.datetime.now()
    print(t.strftime("%Y-%m-%d %H:%M:%S"))


# In[8]:


def mono_preprocess(mono_mass_arr,ppm_shift):
    mono_mass_arr = copy.deepcopy(mono_mass_arr)
    mono_mass_arr.iloc[:,0] = cal_mz(mono_mass_arr.iloc[:,0],ppm_shift)
    return mono_mass_arr


# In[9]:


def get_UE_output(mono_mass_arr,protein,n_terminal_frag_type,c_terminal_frag_type,internal_frag_type,terminal_mass_error,internal_mass_error,unloc_mod_df):
    N_Terminal_CM_output = get_Nterminal_CM_output(mono_mass_arr,protein,n_terminal_frag_type,terminal_mass_error,unloc_mod_df)
    C_Terminal_CM_output = get_Cterminal_CM_output(mono_mass_arr,protein,c_terminal_frag_type,terminal_mass_error,unloc_mod_df)
    Terminal_CM_output = pd.concat([N_Terminal_CM_output,C_Terminal_CM_output],ignore_index=True)
    Internal_CM_output = get_internal_CM_output(mono_mass_arr,protein,internal_frag_type,internal_mass_error,unloc_mod_df)#ax,by,cz离子相同，只保留ax离子 
    output_columns = ["Frag Type","Observed Mass","Theoretical Mass","Start AA","End AA","Error","Fixed Mod","Unlocalized Mod","Sequence","Intensity","Formula","Charge","mz"]
    UE_output = pd.DataFrame(np.vstack([Terminal_CM_output.values,Internal_CM_output.values]),columns = output_columns)
    return UE_output


# In[10]:


def get_UE_output_terminal(mono_mass_arr,protein,n_terminal_frag_type,c_terminal_frag_type,terminal_mass_error,unloc_mod_df):
    N_Terminal_CM_output = get_Nterminal_CM_output(mono_mass_arr,protein,n_terminal_frag_type,terminal_mass_error,unloc_mod_df)
    C_Terminal_CM_output = get_Cterminal_CM_output(mono_mass_arr,protein,c_terminal_frag_type,terminal_mass_error,unloc_mod_df)
    Terminal_CM_output = pd.concat([N_Terminal_CM_output,C_Terminal_CM_output],ignore_index=True)
    #Internal_CM_output = get_internal_CM_output(mono_mass_arr,protein,[],add_H,ppm)#ax,by,cz离子相同，只保留ax离子 
    #不能直接concat，columns匹配会错误。
    output_columns = ["Frag Type","Observed Mass","Theoretical Mass","Start AA","End AA","Error","Fixed Mod","Unlocalized Mod","Sequence","Intensity","Formula","Charge","mz"]
    UE_output = pd.DataFrame(Terminal_CM_output.values,columns = output_columns)
    return UE_output


# In[11]:


def get_terminal_error(UE_output_terminal):
    return np.mean(UE_output_terminal["Error"])


# In[12]:


def read_param(param_dir):
    with open(param_dir,mode="r",encoding="utf-8") as f:
        yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)
    return yamlConf


# In[13]:


def add_mod(protein,mod_df):
    for _,item in mod_df.iterrows():
        mod = Mod(name = item["name"],formula = item["formula"],loc = item["loc"],_mass = mass.calculate_mass(formula=item["formula"]))
        protein += mod
    return protein


# In[14]:


def get_unloc_mod_df(file_dir):
    mod_df = pd.read_csv(file_dir,)


# In[15]:


#读写参数的PANDA-UV参数的类
class paramClass:
    def __init__(self):
        #保存参数的路径
        self.dir = "."
        #保存参数的文件名字
        self.filename = "PANDA-UV_param.yaml"
        self.param_output_dir = self.dir+"/"+self.filename
        self.param_dict = self.get_param_template()
        
    #生成一个空白的PANDA-UV配置文件
    def get_param_template(self):
        param_dict = {"sequence":'',"deconv_mass_file_dir":'',"fixed_mod_file_dir":'',"unlocalized_mod_file_dir":'',"r_env_dir":'',
                      "mass_calibration":True,"ms_calibration":True,"mass_mode":'',"terminal_mass_error":10,
                      "internal_mass_error":10,"peak_match_error":10,"n_terminal_frag_type":[],"c_terminal_frag_type":[],
                      "internal_frag_type":[],"workplace_dir":'',"mzml_file_dir":''}
        return param_dict
    
    #输入python数据结构对象，保存到当前目录的默认参数文件夹中
    def save_param(self,param_dict=None,param_output_dir=None):
        #如果没有输入参数，则默认保存模板
        if param_dict is None:
            param_dict = self.param_dict
        else:
            pass
        
        if param_output_dir is None:
            param_output_dir = self.param_output_dir
        else:
            pass
        
        with open(self.param_output_dir,encoding="utf-8",mode="w") as f:
            yaml.dump(param_dict,f)
    
    def read_param(self,param_input_dir=None):
        #没有输入路径时默认读取模板
        if param_input_dir is None:
            param_input_dir = self.param_output_dir
        else:
            pass
        
        if os.path.isfile(param_input_dir):
            with open(param_input_dir,mode="r",encoding="utf-8") as f:
                try:
                    yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)
                except Exception as exp:
                    print(exp)
                else:
                    self.param_dict = yamlConf
        else:
            pass
    #设置param_dict属性
    def set_param(self,param_dict):
        self.param_dict = param_dict


# In[16]:


def main(param_dict):
    r_env_dir = param_dict["r_env_dir"]
    test_seq = param_dict["sequence"]
    fixed_mod_dir = param_dict["fixed_mod_file_dir"]
    unlocalized_mod_file_dir = param_dict["unlocalized_mod_file_dir"]
    mass_calibration = param_dict["mass_calibration"]
    ms_calibration = param_dict["ms_calibration"]
    deconv_mass_dir = param_dict["deconv_mass_file_dir"]
    peak_match_error = param_dict["peak_match_error"]
    mzml_dir = param_dict["mzml_file_dir"]
    spec_num_i = param_dict["scan_id"]
    mass_mode = param_dict["mass_mode"]
    n_terminal_frag_type = param_dict["n_terminal_frag_type"]
    c_terminal_frag_type = param_dict["c_terminal_frag_type"]
    terminal_mass_error = param_dict["terminal_mass_error"]
    internal_frag_type = param_dict["internal_frag_type"]
    internal_mass_error = param_dict["internal_mass_error"]
    workplace_dir = param_dict["workplace_dir"]

    import os
    os.environ["R_HOME"] = r_env_dir
    import rpy2.robjects as robjects
    print_time()
    first_mass_match_ppm = 20

    test_protein = Protein(test_seq)

    fixed_mod_df = None
    if isinstance(fixed_mod_dir,str):
        if len(fixed_mod_dir)==0:
            print("No fixed mod.")
        else:
            if os.path.isfile(fixed_mod_dir):
                fixed_mod_df = pd.read_csv(fixed_mod_dir)
                test_protein = add_mod(test_protein,fixed_mod_df)
                print("Adding fixed mod...")
            else:
                assert False,print(f"Invalid fixed mod file:{fixed_mod_dir}")
    else:
        pass
    unloc_mod_df = None
    if isinstance(unlocalized_mod_file_dir,str):
        if len(unlocalized_mod_file_dir)==0:
            print("No unlocalized mod.")
        else:
            if os.path.isfile(unlocalized_mod_file_dir):
                unloc_mod_df = pd.read_csv(unlocalized_mod_file_dir)
            else:
                assert False,print(f"Invalid unlocalized mod file:{unlocalized_mod_file_dir}")
    else:
        pass

    precursor_formula = test_protein.FORMULA#已更改enviPat的R脚本，不再输入M+H的分子式

    seqLen = test_protein.SEQLEN

    print("Sequence: ",test_protein)
    print("Length: ",seqLen)
    print("Mass: ",test_protein.MASS)

    mono_mass_arr = pd.read_csv(deconv_mass_dir)
    if mass_calibration:
        output_filename = "fragment_mataching_result_shift.csv"
    else:
        output_filename = "fragment_mataching_result_ori.csv"


    ms_peak_arr = get_ms_peak_arr(mzml_dir,spec_num_i)
    print(f"Initiating R environment: {os.environ['R_HOME']}")
    r_source = robjects.r#初始化R脚本
    r_source(r_script)
    '''#使用母离子偏差作为质量偏差
    if how_cal_error=="precursor":
        precursor_peak_shift_ppm = get_precursor_err(iso_mz_int_arr,ms_mz_int_arr,peak_match_ppm)
        print(f"母离子偏移：{precursor_peak_shift_ppm}")'''

    if mass_mode == "M":
        pass
    elif mass_mode == "MH+":
        #默认第一列是质量
        mono_mass_arr.iloc[:,0] -= 1.00782503207
    else:
        assert False,print(f"Invalid mass mode:{mass_mode}")

    terminal_frag_type = n_terminal_frag_type+c_terminal_frag_type
    UE_output_terminal = get_UE_output_terminal(mono_mass_arr,test_protein,n_terminal_frag_type,c_terminal_frag_type,first_mass_match_ppm,unloc_mod_df)

    precursor_peak_shift_ppm = get_terminal_error(UE_output_terminal)
    print(f"Mass shift of terminal fragments: {precursor_peak_shift_ppm}")
    if mass_calibration:
        mass_shift_ppm = precursor_peak_shift_ppm
        mono_mass_arr_shift = mono_preprocess(mono_mass_arr,mass_shift_ppm)
    else:
        mass_shift_ppm = 0
        mono_mass_arr_shift = mono_mass_arr
    print(f"Mass shift of deconvoluted fragments: {mass_shift_ppm} ppm")
    if ms_calibration:
        ms_peak_arr_shift = mz_shift(ms_peak_arr,precursor_peak_shift_ppm)
        print(f"Spectral shift: {precursor_peak_shift_ppm} ppm")
    else:
        ms_peak_arr_shift = ms_peak_arr
        print(f"Spectral shift: {0} ppm")
    print("Matching fragments....")
    UE_output = get_UE_output(mono_mass_arr_shift,test_protein,n_terminal_frag_type,c_terminal_frag_type,internal_frag_type,terminal_mass_error,internal_mass_error,unloc_mod_df)
    print("PCC scoring....")
    score_term_series = UE_output.apply(lambda x:get_score_term(ms_peak_arr_shift,x,r_source,peak_match_error),axis=1)
    score_term_df = pd.DataFrame(np.vstack(score_term_series),columns = ["PCC","adjust_PCC","dx","dy","peak num","missing peak num"])
    UE_output_with_PCC = pd.concat([UE_output,score_term_df],axis=1)
    
    print("Dropping duplicates....")
    UE_output_s4 = stratage_4.post_process(UE_output_with_PCC,seqLen,0.9,0.3)
    print("Saving result....")
    UE_output_s4.to_csv(f"{workplace_dir}/fragment_matching_result.csv",index=False)
    with open(f"{workplace_dir}/fragment_matching_result_sta.txt",mode="w") as f:
        f.write(get_process_info(UE_output_s4,mono_mass_arr,seqLen))
    print(f"Output dir: {workplace_dir}")
    print_time()
    print("Plotting sequence cleavage maps....")
    seg_map_plot_main(workplace_dir,UE_output_s4,test_seq)
    print("Plotting bar plots of residual fragment yield....")
    fragment_abundance_plot_main(workplace_dir,UE_output_s4,test_seq)
    print("Done. ")


# In[17]:


if __name__=="__main__":
    param = paramClass()
    param.read_param(r"example_param.yaml")
    param_dict = param.param_dict
    main(param_dict)

