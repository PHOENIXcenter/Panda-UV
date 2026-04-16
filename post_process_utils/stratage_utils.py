def get_terminal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]==np.array([1,seqLen])
    return ions_df[np.any(flag_index,axis=1)]
def get_internal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]!=np.array([1,seqLen])
    return ions_df[np.all(flag_index,axis=1)]

def rep_match_QC(ions_df,PCC_thr,Error_thr):
    #PCC_thr = 0.9
    #Error_thr = 3
    PCC_index = ions_df["adjust_PCC"]>=PCC_thr
    Error_index = abs(ions_df["Error"])<=Error_thr
    final_index = PCC_index&Error_index
    return ions_df[final_index]


def get_high_PCC_df(ions_df):
    #按照PCC降序
    highest_PCC = sorted(ions_df["adjust_PCC"])[-1]
    return ions_df[ions_df["PCC"]==highest_PCC]

def get_low_Error_df(ions_df):
    lowest_er = sorted(abs(ions_df["Error"]))[0]
    return ions_df[ions_df["Error"]==lowest_er]