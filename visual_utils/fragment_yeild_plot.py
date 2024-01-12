import plotly.graph_objs as go
import pandas as pd

from plotly.offline import plot

import plotly.express as px

import numpy as np

import sys

import copy

#sys.path.append(r"D:\software\jupyter\BPRC\DICP\UVPD_Explorer\230525-PANDA-UV 1.0")

from ion_match_utils.utils import get_CM_output,save_CM_output,get_terminal_frag_df,get_internal_frag_df

#计算Intensity的总和
def get_TIC(ions_df)->float:
    return np.sum(ions_df["Intensity"])

#计算每个终端离子在序列的相对位置
def get_terminal_relative_AA_site(ions_df,seqLen)->pd.Series:
    AA_site_series = pd.Series(0,index=ions_df.index)
    N_ions_df = ions_df[ions_df["Start AA"]==1]
    C_ions_df = ions_df[ions_df["End AA"]==seqLen]
    #默认相对位置从0开始，但是需要改成从1开始。zhuyl,230624
    AA_site_series[N_ions_df.index] = N_ions_df["End AA"]
    AA_site_series[C_ions_df.index] = C_ions_df["Start AA"]-1
    return AA_site_series

def get_terminal_abundance_fig(ions_df,seqLen):
    fig = px.bar(ions_df, x="Backbone position", y="Intensity", color="Frag Type")
    #terminal_bar_trace = fig.data
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',
                     mirror=True, title_font=dict(size=25), tickfont=dict(size=25))
    fig.update_xaxes(range=[0, seqLen])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',
                     mirror=True, title_font=dict(size=25), tickfont=dict(size=25), showticklabels= True)
    fig.update_layout(title_font_family='Arial', title_x=0.5, title_font=dict(
        size=25), legend_font=dict(size=25))
    fig.update_layout(template='seaborn', plot_bgcolor = 'white')
    fig.update_traces(marker=dict(
        pattern_solidity=0.4, pattern_fgcolor='black'))
    return fig

#将内部离子拆分成为互补的终端离子，然后再绘制强度图
#互补的终端离子在计算Start AA或者End AA时不再是内部离子的Start AA和End AA，需要改变。--zhuyl,230624
def split_internal_to_terminal(internal_ions_df_i,seqLen):
    ion_type = internal_ions_df_i["Frag Type"]
    C_ion_type = ion_type[0]
    N_ion_type = ion_type[1]
    C_ions_df_i = copy.deepcopy(internal_ions_df_i)
    N_ions_df_i = copy.deepcopy(internal_ions_df_i)
    C_ions_df_i["Frag Type"] = C_ion_type
    C_ions_df_i["End AA"] = internal_ions_df_i["Start AA"]-1#和内部离子互补的氨基酸位置--zhuyl,230624
    C_ions_df_i["Start AA"] = 1
    N_ions_df_i["Frag Type"] = N_ion_type
    N_ions_df_i["Start AA"] = internal_ions_df_i["End AA"]+1#和内部离子互补的氨基酸位置--zhuyl,230624
    N_ions_df_i["End AA"] = seqLen
    return C_ions_df_i,N_ions_df_i

def fragment_abundance_plot_main(workplace_dir,ions_df,seq):
    seqLen = len(seq)
    #获取终端离子
    terminal_frag_df = get_terminal_frag_df(ions_df,seqLen).sort_values("Frag Type")
    terminal_frag_df_PCC = copy.deepcopy(terminal_frag_df[terminal_frag_df["adjust_PCC"]>=0.6]).sort_values("Frag Type")
    #获取终端离子的相对碎裂位置
    terminal_relative_AA_site = get_terminal_relative_AA_site(terminal_frag_df,seqLen)
    terminal_relative_AA_site_PCC = get_terminal_relative_AA_site(terminal_frag_df_PCC,seqLen)
    #将相对位置加入df
    terminal_frag_df["Backbone position"] = terminal_relative_AA_site
    terminal_frag_df_PCC["Backbone position"] = terminal_relative_AA_site_PCC
    
    #或取出终端离子的abundance fig
    termianl_abundance_fig = get_terminal_abundance_fig(terminal_frag_df,seqLen)
    termianl_abundance_fig_PCC = get_terminal_abundance_fig(terminal_frag_df_PCC,seqLen)
    
    #仅保存
    plot(termianl_abundance_fig,filename=fr"{workplace_dir}/terminal_abundance_map.html", auto_open=False,include_plotlyjs=True)
    plot(termianl_abundance_fig_PCC,filename=fr"{workplace_dir}/terminal_abundance_map_PCC.html", auto_open=False,include_plotlyjs=True)
    
    internal_frag_df = get_internal_frag_df(ions_df,seqLen)
    
    split_internal_df = pd.DataFrame(columns=internal_frag_df.columns)
    for _,internal_frag_df_i in internal_frag_df.iterrows():
        split_internal_df_i_1,split_internal_df_i_2 = split_internal_to_terminal(internal_frag_df_i,seqLen)
        split_internal_df = split_internal_df.append([split_internal_df_i_1,split_internal_df_i_2])
    split_internal_df.reset_index(inplace=True)
    internal_relative_AA_site = get_terminal_relative_AA_site(split_internal_df,seqLen)
    #PCC>0.9的内部离子产率图
    split_internal_df["Backbone position"] = internal_relative_AA_site
    split_internal_df_PCC = split_internal_df[split_internal_df["adjust_PCC"]>=0.8]
    internal_abundance_fig = get_terminal_abundance_fig(split_internal_df.sort_values("Frag Type"),seqLen)
    internal_abundance_fig_PCC = get_terminal_abundance_fig(split_internal_df_PCC.sort_values("Frag Type"),seqLen)
    #plot(termianl_abundance_fig)
    #仅保存
    plot(internal_abundance_fig,filename=fr"{workplace_dir}/internal_abundance_map.html", auto_open=False,include_plotlyjs=True)
    plot(internal_abundance_fig_PCC,filename=fr"{workplace_dir}/internal_abundance_map_PCC.html", auto_open=False,include_plotlyjs=True)    
    
if __name__=="__main__":
    CA_seq = "SHHWGYGKHNGPEHWHKDFPIANGERQSPVDIDTKAVVQDPALKPLALVYGEATSRRMVNNGHSFNVEYDDSQDKAVLKDGPLTGTYRLVQFHFHWGSSDDQGSEHTVDRKKYAAELHLVHWNTKYGDFGTAAQQPDGLAVVGVFLKVGDANPALQKVLDALDSIKTKGKSTDFPNFDPGSLLPNVLDYWTYPGSLTTPPLLESVTWIVLKEPISVSSQQMLKFRTLNFNAEGEPELLMLANWRPAQPLKNRQVRGFPK"
    Ub_seq = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
    Mb_seq = "GLSDGEWQQVLNVWGKVEADIAGHGQEVLIRLFTGHPETLEKFDKFKHLKTEAEMKASEDLKKHGTVVLTALGGILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISDAIIHVLHSKHPGDFGADAQGAMTKALELFRNDIAAKYKELGFQG"
    M_apple_seq = "MVSKGEENNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEAFQTAKLKVTKGGPLPFAWDILSPQFMYGSKVYIKHPADIPDYFKLSFPEGFRWERVMNFEDGGIIHVNQDSSLQDGVFIYKVKLRGTNFPSDGPVMQKKTMGWEASEERMYPEDGALKSEIKKRLKLKDGGHYAAEVKTTYKAKKPVQLPGAYIVDIKLDIVSHNEDYTIVEQYERAEGRHSTGGMDELYKGSAFKLEHHHHHH"
    M_apple_67_AMF_seq = "VSKGEENNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEAFQTAKLKVTKGGPLPFAWDILSPQFMYGSKVYIKHPADIPDYFKLSFPEGFRWERVMNFEDGGIIHVNQDSSLQDGVFIYKVKLRGTNFPSDGPVMQKKTMGWEASEERMYPEDGALKSEIKKRLKLKDGGHYAAEVKTTYKAKKPVQLPGAYIVDIKLDIVSHNEDYTIVEQYERAEGRHSTGGMDELYKGSAFKLEHHHHHH"

    #NTerm_ion_type = ["x","y","x+1","y-1","z+1"]
    #CTerm_ion_type = ["a","b","c","a+1"]
    #internal_ion_type = ["ax","ay","az+2","bx","bz+2","cx","cy"]
    #ion_type_color_map = {"red":["a","x","x+1","a+1"],"green":["b","y","y-1"],"blue":["c","z+1"]}
    msalign_dir= r"F:\JUPYTER\BPCR\DICP\ClipsMS\UE_output_230621\CA_shift"
    #msalign_dir = r"F:\JUPYTER\BPCR\DICP\ClipsMS\UE_output_230615\M_Apple"
    #存放三个文件的文件夹名，该文件夹下包含mzml,msalign,raw这三个文件
    #msalign_filename= r"20220411_NativeCA_UVPD193_Z10_AT1_1"
    #msalign_filename = "20230330_M_Apple_UVPD_193_1_5MJ_Z11_2591_4"
    msalign_filename = "20220411_NativeCA_UVPD193_Z10_AT1_1"

    test_seq = CA_seq
    seqLen = len(test_seq)
    input_dir = f"{msalign_dir}/{msalign_filename}"
    spec_num_i = 0
    filename = "UE_output_s4.csv"
    CA_output_s4 = get_CM_output(input_dir,spec_num_i,"UE_output_s4.csv")
    CA_output_s2 = get_CM_output(input_dir,spec_num_i,"UE_output_s2.csv")
    CA_output_s1 = get_CM_output(input_dir,spec_num_i,"UE_output_s1.csv")
    TIC=1
    fragment_abundance_plot_main(input_dir,spec_num_i,CA_output_s1,test_seq)