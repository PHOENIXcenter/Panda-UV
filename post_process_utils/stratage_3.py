import pandas as pd
import numpy as np
import copy

def get_terminal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]==np.array([1,seqLen])
    return ions_df[np.any(flag_index,axis=1)]
def get_internal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]!=np.array([1,seqLen])
    return ions_df[np.all(flag_index,axis=1)]
#保留所有终端离子，保留PCC>0.9的内部离子
def post_process(ions_df,seqLen,QC_PCC_thr,QC_Error_thr):
    terminal_ions_df = get_terminal_frag_df(ions_df,seqLen)
    internal_ions_df = get_internal_frag_df(ions_df,seqLen)
    
    PCC_index = internal_ions_df["adjust_PCC"]>=QC_PCC_thr
    internal_ions_df_processed = internal_ions_df[PCC_index]
    
    return pd.concat([terminal_ions_df,internal_ions_df_processed])