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

def rep_match_QC(ions_df,PCC_thr,Error_thr):
    #PCC_thr = 0.9
    #Error_thr = 3
    PCC_index = ions_df["adjust_PCC"]>=PCC_thr
    Error_index = abs(ions_df["Error"])<=Error_thr
    final_index = PCC_index&Error_index
    return ions_df[final_index]


def get_high_PCC_df(ions_df):
    #按照PCC升序
    highest_PCC = sorted(ions_df["adjust_PCC"])[-1]
    return ions_df[ions_df["adjust_PCC"]==highest_PCC]

def get_low_Error_df(ions_df):
    lowest_er = sorted(abs(ions_df["Error"]))[0]
    return ions_df[abs(ions_df["Error"])==lowest_er]#进行值的匹配时也需要进行abs，否则匹配不到Error为负的最小Error离子--zhuyl,230526 

#处理一个实验离子匹配上多个终端离子或者内部离子的情况
#不对输入进行检查
#优先选择Error低的离子，最低Error离子有多个，且PCC相同则全部保留
def process_terminal_rep_match(ions_df,QC_PCC_thr,QC_Error_thr):
    #获取误差最小的离子
    final_ions_df = get_low_Error_df(ions_df)
    #如果匹配上多个低误差离子
    if len(final_ions_df)>1:
        #则选取PCC高的离子
        final_ions_df = get_high_PCC_df(final_ions_df)
        #如果还有多个离子
        #if len(final_ions_df)>1:
            #此时使用所有特征进行质控，如果所有离子都满足要求则保留所有离子
        #    final_ions_df = rep_match_QC(final_ions_df,QC_PCC_thr,QC_Error_thr)
    return final_ions_df

#处理一个实验离子匹配上多个理论离子的情况
#输入分组之后的数据，按组处理
#再将分组之后的数据按照终端离子和内部离子分别处理
#终端离子的选择策略，输入的是根据去卷积离子分组之后的匹配结果
#如果只有一个终端离子则返回这个终端离子
#如果有多个终端离子，则选择Error最小的，Error最小的离子有多个且PCC相同，则全部保留
#如果只有多个内部离子，则选择Error最小的，Error最小的离子有多个且PCC相同，则全部保留。相比策略1减少了最终同时保留相同分子式的限制。
def process_rep_match(ions_df,seqLen,QC_PCC_thr,QC_Error_thr):
    terminal_df = get_terminal_frag_df(ions_df,seqLen)
    internal_df = get_internal_frag_df(ions_df,seqLen)
    final_ions_df = internal_df
    #如果只有一个终端离子，则返回这个终端离子
    if len(terminal_df) == 1:
        final_ions_df = terminal_df
        return final_ions_df
    #处理匹配上多个终端离子的情况
    elif len(terminal_df) >1:
        final_ions_df = process_terminal_rep_match(terminal_df,QC_PCC_thr,QC_Error_thr)
        return final_ions_df
    
    #如果只有一个内部离子则直接返回这个内部离子
    if len(internal_df) == 1:
        final_ions_df = internal_df
        return internal_df
    elif len(internal_df) > 1:
        final_ions_df = process_terminal_rep_match(internal_df,QC_PCC_thr,QC_Error_thr)
    return final_ions_df

#重复匹配时选择终端离子
def post_process(ions_df,seqLen,QC_PCC_thr,QC_Error_thr):
    all_columns = ions_df.columns
    
    #用于分组的列名。去卷积离子所有的属性
    group_columns = ["Observed Mass", "Intensity", "Charge", "mz"]
    #其余的列名。除了去卷积离子属性的其余所有蛋白的属性。
    #other_columns = list(filter(lambda x:x not in group_columns,all_columns))
    
    #对输出进行分组
    g = ions_df.groupby(group_columns)
    final_ions_df = pd.DataFrame(columns = all_columns)
    for name,_ in g:
        #处理每一组的匹配离子
        #获取按照实验离子分组的UE_output
        group_ions_df = g.get_group(name)
        #只匹配到了一个理论离子，则直接添加到结果中
        if len(group_ions_df)==1:
            tmp_ions_df = group_ions_df
            final_ions_df = final_ions_df.append(tmp_ions_df,ignore_index=True)
            #tmp_ions_df = tmp_ions_df.append(group_ions_df)
        #匹配到了多个离子则使用质控策略
        #分组之后肯定取值不会为空表格
        else:
            #pass
            tmp_ions_df = process_rep_match(group_ions_df,seqLen,QC_PCC_thr,QC_Error_thr)
            final_ions_df = final_ions_df.append(tmp_ions_df,ignore_index=True)
        #final_ions_df = final_ions_df.append(tmp_ions_df,ignore_index=True)
        
        #break
    return final_ions_df