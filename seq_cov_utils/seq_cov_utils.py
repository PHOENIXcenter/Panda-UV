import numpy as np
import copy
#根据ions_df和seqLen计算序列覆盖率
#获取在N端和C-碎裂的位点
#根据seqLen获取内部离子和终端离子
def get_terminal_frag_df_index(ions_df,seqLen):
    flag_index = ions_df[["Start AA","End AA"]]==np.array([1,seqLen])
    return np.any(flag_index,axis=1)
def get_internal_frag_df_index(ions_df,seqLen):
    flag_index = ions_df[["Start AA","End AA"]]!=np.array([1,seqLen])
    return np.all(flag_index,axis=1)

def get_terminal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]==np.array([1,seqLen])
    return ions_df[np.any(flag_index,axis=1)]
def get_internal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]!=np.array([1,seqLen])
    return ions_df[np.all(flag_index,axis=1)]

def get_N_terminal_seg_site(ions_df,seqLen):
    term_ions_df = get_terminal_frag_df(ions_df,seqLen)
    seg_site_arr = np.zeros(shape=seqLen-1,dtype=int)#不包括完整蛋白质的离子
    NTerm_seg_site_index = term_ions_df[(term_ions_df["Start AA"]==1)&(term_ions_df["End AA"]<seqLen)]["End AA"]
    for i in NTerm_seg_site_index.values:
        seg_site_arr[int(i-1)]+=1
    return seg_site_arr

#获取在C端碎裂的位点
def get_C_terminal_seg_site(ions_df,seqLen):
    term_ions_df = get_terminal_frag_df(ions_df,seqLen)
    seg_site_arr = np.zeros(shape=seqLen-1,dtype=int)#不包括完整蛋白质的离子
    CTerm_seg_site_index = term_ions_df[(term_ions_df["Start AA"]>1)&(term_ions_df["End AA"]==seqLen)]["Start AA"]
    for i in CTerm_seg_site_index.values:
        seg_site_arr[int(i-2)]+=1 
    return seg_site_arr

def get_terminal_seg_site(ions_df,seqLen):
    return get_N_terminal_seg_site(ions_df,seqLen)+get_C_terminal_seg_site(ions_df,seqLen)

def get_internal_seg_site(ions_df,seqLen):
    int_ions_df = get_internal_frag_df(ions_df,seqLen)
    seg_site_arr = np.zeros(shape=seqLen-1,dtype=int)
    seg_site_index = int_ions_df[["Start AA","End AA"]].values
    for i,j in seg_site_index:
        seg_site_arr[int(j-1)]+=1
        seg_site_arr[int(i-2)]+=1
    return seg_site_arr

def get_matched_frags(ions_df):
    frag_mass = set(ions_df["Observed Mass"])
    return frag_mass

def get_mono_mass_num(mono_mass_arr):
    return len(mono_mass_arr)

def get_seq_conv(ions_df,seqLen):
    internal_seg_site = get_internal_seg_site(ions_df,seqLen)
    terminal_seg_site = get_terminal_seg_site(ions_df,seqLen)
    site_index = (internal_seg_site+terminal_seg_site)>0
    return sum(site_index)/len(site_index)