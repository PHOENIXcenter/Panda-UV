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

from post_process_utils.post_process import post_process_and_save

from visual_utils.site_map_plot import seg_map_plot_main
from visual_utils.fragment_yeild_plot import fragment_abundance_plot_main


# In[2]:


import datetime


# In[3]:


import sys


# In[4]:


import yaml


# In[5]:


#计算理论同为素峰的R脚本
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


#计算谱图偏移后的单同位素质量
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
    #不能直接concat，columns匹配会错误。
    output_columns = ["Frag Type","Observed Mass","Theoretical Mass","Start AA","End AA","Error","Fixed Mod","Unlocalized Mod","Sequence","Intensity","Formula","Charge","mz"]
    UE_output = pd.DataFrame(np.vstack([Terminal_CM_output.values,Internal_CM_output.values]),columns = output_columns)
    return UE_output


# In[10]:


#计算终端离子，用于计算离子偏移
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


#给序列添加固定修饰
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
        
        with open(param_input_dir,mode="r",encoding="utf-8") as f:
            yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.param_dict = yamlConf
        #return yamlConf
    
    #设置param_dict属性
    def set_param(self,param_dict):
        self.param_dict = param_dict


# In[16]:


#输入参数字典，运行主程序
def main(param_dict):
    #打印当前时间
    #print_time()
    #从指定路径读取参数，这一行和.py文件不同其他地方需要保持一致。
    #param = read_param(r"F:\JUPYTER\BPCR\DICP\PANDA-UV_paper_data_analysis\Paper_materials\mAbs\230904-Infliximab\HC_Fc_2\Infliximab_HC_Fc_2_param.yaml")

    #R环境的位置
    r_env_dir = param_dict["r_env_dir"]
    test_seq = param_dict["sequence"]
    fixed_mod_dir = param_dict["fixed_mod_file_dir"]
    unlocalized_mod_file_dir = param_dict["unlocalized_mod_file_dir"]
    mass_calibration = param_dict["mass_calibration"]#匹配离子时是否矫正质量
    ms_calibration = param_dict["ms_calibration"]#计算PCC时是否进行谱图矫正计算
    deconv_mass_dir = param_dict["deconv_mass_file_dir"]
    peak_match_error = param_dict["peak_match_error"]#PCC打分时谱峰匹配的误差
    mzml_dir = param_dict["mzml_file_dir"]
    spec_num_i = param_dict["scan_id"]
    mass_mode = param_dict["mass_mode"]
    n_terminal_frag_type = param_dict["n_terminal_frag_type"]
    c_terminal_frag_type = param_dict["c_terminal_frag_type"]
    terminal_mass_error = param_dict["terminal_mass_error"]
    internal_frag_type = param_dict["internal_frag_type"]
    internal_mass_error = param_dict["internal_mass_error"]
    workplace_dir = param_dict["workplace_dir"]

    #在主函数中指定R路径，保证R路径改变之后初始化R环境能初始化新的R环境--zhuyl,230814
    import os
    os.environ["R_HOME"] = r_env_dir
    import rpy2.robjects as robjects
    #打印当前时间
    print_time()
    #从指定路径读取参数，这一行和.py文件不同其他地方需要保持一致。
    #param = read_param(r"D:\software\jupyter\BPRC\DICP\内部离子表征蛋白质结构-230623\Mb_apo_test_abundance_plot_fixed-230726\Mb_apo_param.yaml")

    #如何计算误差，str: precursor or terminal
    #how_cal_error = "terminal"
    #计算偏差时匹配终端离子的质量误差范围
    first_mass_match_ppm = 20

    #使用enviPat的R脚本
    #r_script_dir = param["r_script_dir"]，停止使用外部R脚本，直接在程序内初始化--zhuyl，230814
    #r_script_dir = fr"{r_script_dir}"
    #匹配193CA的终端离子，看能否和Prosight对应

    #Trastuzumab_ppm_shift = -1.34983241
    #ppm_shift=-1.34983241
    #msalign_dir = param_dict["msalign_dir"]
    #msalign_dir = fr"{msalign_dir}"
    #msalign_filename = param_dict["msalign_filename"]
    #spec_num_i = param_dict["spec_num_i"]

    test_protein = Protein(test_seq)
    #如果存在修饰文件

    #fixed_mod_dir = fr"{fixed_mod_dir}"
    #如果存在修饰文件则添加修饰到蛋白
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
    #读取unloc_mod文件--zhuyl,231113
    unloc_mod_df = None
    if isinstance(unlocalized_mod_file_dir,str):
        if len(unlocalized_mod_file_dir)==0:
            print("No unlocalized mod.")
        else:
            if os.path.isfile(unlocalized_mod_file_dir):
                unloc_mod_df = pd.read_csv(unlocalized_mod_file_dir)
                #test_protein = add_mod(test_protein,mod_df)
                #print("Adding fixed mod...")
            else:
                assert False,print(f"Invalid unlocalized mod file:{unlocalized_mod_file_dir}")
    else:
        pass

    #匹配holo离子时按照Mb_apo分子式进行矫正
    precursor_formula = test_protein.FORMULA#已更改enviPat的R脚本，不再输入M+H的分子式

    #precursor_charge = param["precursor_charge"]，计算离子质量偏移使用终端离子的平均误差，zhuyl--230814
    seqLen = test_protein.SEQLEN

    #add_H = param_dict["add_H"]#是否以[M+H]+模式从msalign文件读取单同位素质量,需要和离子匹配模式统一。同时也需要和FragIon_IsoPatterna_copy.R脚本同步，因为默认输入的是[M+H]+模式
    print("蛋白序列：",test_protein)
    print("蛋白长度：",seqLen)
    print("蛋白质量：",test_protein.MASS)
    #terminal_mass_error = param_dict["terminal_mass_error"]#离子匹配误差
    #terminal_mass_error = param_dict["terminal_mass_error"]#离子匹配误差

    #输入文件的位置
    #input_dir = f"{msalign_dir}/{msalign_filename}"
    #获取单同位素质量列表，直接读取为df
    #mono_mass_arr = get_CM_output(input_dir,spec_num_i,"mono_mass_with_charge.csv")
    #mono_mass_arr = get_mono_in_file(input_dir,spec_num_i,add_H)

    mono_mass_arr = pd.read_csv(deconv_mass_dir)
    #标准格式保存使用的单同位素质量列表
    #save_CM_output(mono_mass_arr,input_dir,spec_num_i,"mono_mass_with_charge.csv")
    #如果偏移了质量则保存为shift后缀的输出文件，如果没有偏移则保存为ori后缀文件
    if mass_calibration:
        output_filename = "UE_output_shift.csv"
    else:
        output_filename = "UE_output_ori.csv"

    #根据母离子分子式和电荷计算谱图偏移ppm，要输入+H的分子式
    #不再输入M+H分子式，zhuyl--230814
    #ms_mz_int_arr = get_spec_i_mz_arr(input_dir,spec_num_i)#获取mzml的谱峰信息

    ms_peak_arr = get_ms_peak_arr(mzml_dir,spec_num_i)
    print(f"初始化R环境：{os.environ['R_HOME']}")
    #print(f"初始化enviPat脚本：{r_script_dir}")
    r_source = robjects.r#初始化R脚本
    r_source(r_script)
    #根据蛋白质序列和电荷获取同位素分布，一定要输入M+H的分子式
    #现在只用输入M的分子式即可
    #iso_mz_int_arr = get_iso_arr(r_source,precursor_formula,precursor_charge)，只使用终端离子的平均误差作为质量偏移值
    '''#使用母离子偏差作为质量偏差
    if how_cal_error=="precursor":
        precursor_peak_shift_ppm = get_precursor_err(iso_mz_int_arr,ms_mz_int_arr,peak_match_ppm)
        print(f"母离子偏移：{precursor_peak_shift_ppm}")'''
    #只使用终端离子误差作为偏移值--zhuyl,230908
    #elif how_cal_error=="terminal":

    if mass_mode == "M":
        pass
    elif mass_mode == "MH+":
        #默认第一列是质量
        mono_mass_arr.iloc[:,0] -= 1.00782503207
    else:
        assert False,print(f"Invalid mass mode:{mass_mode}")

    terminal_frag_type = n_terminal_frag_type+c_terminal_frag_type
    #第一次匹配使用较大的误差，谱图矫正之后使用较小的误差匹配
    #匹配离子时加入unloc_mod_df，用于匹配非固定修饰--zhuyl, 231114
    UE_output_terminal = get_UE_output_terminal(mono_mass_arr,test_protein,n_terminal_frag_type,c_terminal_frag_type,first_mass_match_ppm,unloc_mod_df)

    precursor_peak_shift_ppm = get_terminal_error(UE_output_terminal)
    print(f"终端离子偏移：{precursor_peak_shift_ppm}")
    #else:
    #    assert False,f"Error flag invalid: {how_cal_error}"
    #指定Mb 连接heme之后的质量偏移
    #precursor_peak_shift_ppm = -4.90250478742977
    #Mb的质量偏移
    #precursor_peak_shift_ppm = -5.320348676784102
    #如果需要质量偏移，则计算母离子的偏差，然后将单同位素质量进行偏移
    if mass_calibration:
        #获取质量偏移误差
        mass_shift_ppm = precursor_peak_shift_ppm
        mono_mass_arr_shift = mono_preprocess(mono_mass_arr,mass_shift_ppm)
    #否则偏移量为0
    else:
        mass_shift_ppm = 0
        mono_mass_arr_shift = mono_mass_arr
    #根据整体偏移计算偏移之后的质量
    print(f"单同位素质量偏移：{mass_shift_ppm} ppm")
    #进行谱图偏移，然后计算PCC
    if ms_calibration:
        #使用母离子偏差作为谱图的偏差
        ms_peak_arr_shift = mz_shift(ms_peak_arr,precursor_peak_shift_ppm)
        print(f"谱图偏移：{precursor_peak_shift_ppm} ppm")
    else:
        ms_peak_arr_shift = ms_peak_arr
        print(f"谱图偏移：{0} ppm")
    #mono_mass_arr_shift = mono_preprocess(mono_mass_arr,ppm_shift)
    #ion_type_list = ["a","b","c","x","y","z+1","a+1","x+1","y-1"]
    #使用UE匹配离子，
    print("正在匹配离子....")
    #进行离子匹配
    UE_output = get_UE_output(mono_mass_arr_shift,test_protein,n_terminal_frag_type,c_terminal_frag_type,internal_frag_type,terminal_mass_error,internal_mass_error,unloc_mod_df)
    #保存结果
    print("正在进行PCC打分....")
    score_term_series = UE_output.apply(lambda x:get_score_term(ms_peak_arr_shift,x,r_source,peak_match_error),axis=1)
    score_term_df = pd.DataFrame(np.vstack(score_term_series),columns = ["PCC","adjust_PCC","dx","dy","peak num","missing peak num"])
    UE_output_with_PCC = pd.concat([UE_output,score_term_df],axis=1)
    print("正在保存结果....")
    UE_output_with_PCC.to_csv(f"{workplace_dir}/{output_filename}",index=False)
    #save_CM_output(UE_output_with_PCC,input_dir,spec_num_i,output_filename)
    print("去除重复匹配....")
    #保存几种不同策略过滤结果，包括csv，txt文件保存序列覆盖率等信息
    #0.9和3这两个参数没有使用，已注释，但是为了不更改参数，还是将其传入了函数，实际并没有发挥作用。
    post_process_and_save(UE_output_with_PCC,mono_mass_arr,seqLen,workplace_dir,0.9,3)
    print(f"离子匹配文件输出到：{workplace_dir}/{output_filename}")
    print_time()
    #save_CM_output(UE_output,input_dir,spec_num_i,output_filename)
    #加上PCC打分
    #cal_and_save_one_scan(input_dir,spec_num_i,output_filename,precursor_formula,precursor_charge,r_script_dir,ppm)
    #添加绘制碎裂位点图的功能--zhuyl,230616
    CA_output_s4 = pd.read_csv(fr"{workplace_dir}/UE_output_s4.csv")
    print("绘制碎裂位点图....")
    seg_map_plot_main(workplace_dir,CA_output_s4,test_seq)
    print("绘制离子产率图....")
    fragment_abundance_plot_main(workplace_dir,CA_output_s4,test_seq)
    print("Done. ")


# In[17]:


def batch_main(param_dict,msalign_dir,msalign_filename_list,fixed_mod_file_dir,unlocalized_mod_file_dir,sequence):
    for msalign_filename in msalign_filename_list:
        input_dir = f"{msalign_dir}/{msalign_filename}"
        deconv_mass_file_dir = fr"{input_dir}/ms2_0/mono_mass_with_charge.csv"
        mzml_file_dir = fr"{input_dir}/{msalign_filename}.mzML"
        workplace_dir = fr"{input_dir}/ms2_0"

        param_dict["fixed_mod_file_dir"] = fixed_mod_file_dir
        param_dict["unlocalized_mod_file_dir"] = unlocalized_mod_file_dir
        param_dict["input_dir"] = input_dir    
        param_dict["deconv_mass_file_dir"] = deconv_mass_file_dir    
        param_dict["mzml_file_dir"] = mzml_file_dir    
        param_dict["workplace_dir"] = workplace_dir
        param_dict["sequence"] = sequence
        param_dict = param.param_dict
        main(param_dict)


# In[18]:


if __name__=="__main__":
    param = paramClass()
    param.read_param(r"CA_param.yaml")
    param_dict = param.param_dict
    main(param_dict)