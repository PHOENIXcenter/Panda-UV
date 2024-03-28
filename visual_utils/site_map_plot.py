import pandas as pd
import numpy as np
import os
import sys

import plotly
import plotly.graph_objs as go
from plotly.offline import plot

import math

import copy

#sys.path.append(r"D:\software\jupyter\BPRC\DICP\UVPD_Explorer\230525-PANDA-UV 1.0")

from ion_match_utils.utils import get_CM_output,save_CM_output,get_terminal_frag_df,get_internal_frag_df

from seq_cov_utils.seq_cov_utils import get_seq_conv,get_matched_frags,get_terminal_seg_site,get_internal_seg_site,get_N_terminal_seg_site,get_C_terminal_seg_site
ion_type_color_map = {"red":["a","a+1","a-1","x","x+1","x-1"],"green":["b","y","y-1","y-2"],"blue":["c","c.","z","z+1","z-1"]}
#根据序列获取坐标,横向最长25个氨基酸，竖向10个。比如PEP返回x=[1,2,3],y=[10,10,10]
def get_seq_trace_cor(seq)->[np.ndarray,np.ndarray]:
    #一行容纳的氨基酸个数
    width = 25
    #一页的一列最多能容纳的氨基酸个数
    high = 10
    seqLen = len(seq)
    #实际一列有多少个氨基酸
    real_high = int(seqLen/width)+1
    x_cor_arr = np.tile(np.arange(width),real_high)
    x_cor_arr = x_cor_arr[:seqLen]
    y_cor_arr = np.reshape(np.tile(np.array(list(reversed(np.arange(real_high)))),width),[width,real_high]).T
    y_cor_arr = np.reshape((y_cor_arr),[-1])
    y_cor_arr = y_cor_arr[:seqLen]
    
    return x_cor_arr,y_cor_arr

def get_seq_trace(seq,x_cor_arr,y_cor_arr)->go.Scatter:
    
    #x_cor_arr,y_cor_arr = get_seq_trace_cor(seq)
    #<b>在解析的时候被解释为空格
    seq_list = ['<b>' + aa + '<b>' for aa in seq]
    seqLen = len(seq)
    #当前氨基酸位点的位置
    site_num = list(np.arange(seqLen)+1)
    #选定在氨基酸位点时显示的信息
    hovertext = [AA+str(site_num_i) for AA,site_num_i in zip(list(seq),site_num)]
    seq_trace = go.Scatter(x=x_cor_arr,y=y_cor_arr,
                                       mode="text",
                                       text=seq_list,
                                       textfont = dict(family = 'Arial', size = 40),
                                       textposition="middle center",
                                       hovertext=hovertext,
                                       hoverinfo="text")
    return seq_trace

#根据输入的终端离子，获取碎裂位点坐标位置，不输入离子类型
def get_terminal_seg_trace_cor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)->[float,float]:
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    ion_type = ions_df_i["Frag Type"]
    if start==1 and end<seqLen:
        abs_site = end
        x = x_cor_arr[abs_site-1]+0.5
        y = y_cor_arr[abs_site-1]+0.08
        return x,y
    elif start>1 and end==seqLen:
        abs_site = start
        x = x_cor_arr[abs_site-1]-0.5
        y = y_cor_arr[abs_site-1]+0.08
        return x,y
    else:
        assert False,f"Get invalid terminal ion type {ion_type},start site {start},end site {end}. "
        
def get_termimal_seg_trace(ions_df_i,x,y)->go.Scatter:
    ion_type = ions_df_i["Frag Type"]
    color=None
    for key,value in ion_type_color_map.items():
        if ion_type in value:
            color = key
            break
        else:
            pass
    if color is None:
        assert False,print(f"Invalid ion type: {ion_type}")
    else:
        pass
    
    seg_trace = go.Scatter(x=[x],y=[y],
                        mode = 'markers',
                        marker = dict(symbol = 'line-ns',color = color,size = 25,line = dict(color = color,width = 4)),
                        hoverinfo = 'skip',
                        name=ion_type
                        )
    return seg_trace

def get_internal_seg_trace_cor(ions_df_i,x_cor_arr,y_cor_arr)->np.array:
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    cor_array = np.zeros(shape=[2,2])
    #abs_site = start
    N_x = x_cor_arr[start-1]-0.5
    N_y = y_cor_arr[start-1]+0.08
    C_x = x_cor_arr[end-1]+0.5
    C_y = y_cor_arr[end-1]+0.08
    cor_array[0,0] = N_x
    cor_array[0,1] = N_y
    cor_array[1,0] = C_x
    cor_array[1,1] = C_y
    return cor_array

#返回终端离子的Scatter,一个离子一个Scatter，不分端点
def get_internal_seg_trace(ions_df_i,x_cor_arr,y_cor_arr)->go.Scatter:
    start = ions_df_i["Start AA"]
    end = ions_df_i["End AA"]
    ion_type = ions_df_i["Frag Type"]
    Error = round(ions_df_i["Error"],4)
    PCC = round(ions_df_i["adjust_PCC"],4)
    exp_mass = round(ions_df_i["Observed Mass"],4)
    the_mass = round(ions_df_i["Theoretical Mass"],4)
    Charge = int(ions_df_i["Charge"])
    Intensity = round(ions_df_i["Intensity"],4)
    mz = round(ions_df_i["mz"],4)
    cor_array = get_internal_seg_trace_cor(ions_df_i,x_cor_arr,y_cor_arr)
    trace = go.Scatter(x=cor_array[:,0],y=cor_array[:,1],
                        mode = 'markers',
                        marker = dict(symbol = 'line-ns',color = "purple",size = 25,line = dict(color = "purple",width = 4)),
                        hovertemplate = f'Observed Mass: {exp_mass}Da<br><br>'+
                                         f'AA range: {start},{end}<br>' +
                                             f'Ion Type: {ion_type}<br>' +
                                             f'Theoretical Mass: {the_mass}Da<br>' +
                                             f'PCC: {PCC}<br>'+
                                             f'Error: {Error}ppm<br>'+f'Charge: {Charge}<br>'+f'Intensity: {Intensity}<br>'+f'mz: {mz}<br><extra></extra>',
                       hoveron="points+fills",
                       name=ion_type)
    return trace

def internal_seg_trace_constructor(ions_df_i,x_cor_arr,y_cor_arr):
    seg_trace = get_internal_seg_trace(ions_df_i,x_cor_arr,y_cor_arr)
    return seg_trace


def get_terminal_ion_trace(ions_df_i,x,y)->go.Scatter:
    ion_type = ions_df_i["Frag Type"]
    Error = round(ions_df_i["Error"],4)
    PCC = round(ions_df_i["adjust_PCC"],4)
    exp_mass = round(ions_df_i["Observed Mass"],4)
    the_mass = round(ions_df_i["Theoretical Mass"],4)
    Charge = int(ions_df_i["Charge"])
    Intensity = round(ions_df_i["Intensity"],4)
    mz = round(ions_df_i["mz"],4)
    color=None
    for key,value in ion_type_color_map.items():
        if ion_type in value:
            color = key
            break
        else:
            pass
    if color is None:
        assert False,print(f"Invalid ion type: {ion_type}")
    else:
        pass
    
    if ion_type in ["a","a+1","a-1"]:
        ion_trace_x = x-0.1
        ion_trace_y = y+0.265
        angle = 0
        size=10
    elif ion_type in ["x","x+1","x-1"]:
        ion_trace_x = x+0.1
        ion_trace_y = y-0.265
        angle = 0
        size=10
    elif ion_type in ["b"]:
        ion_trace_x = x-0.11
        ion_trace_y = y+0.35
        angle = 30
        size=12
    elif ion_type in ["y","y-1","y-2"]:
        ion_trace_x = x+0.11
        ion_trace_y = y-0.35
        angle = 30
        size=12
    elif ion_type in ["c","c."]:
        ion_trace_x = x-0.08
        ion_trace_y = y+0.39
        angle = 60
        size=13
    elif ion_type in ["z","z+1","z-1"]:
        ion_trace_x = x+0.08
        ion_trace_y = y-0.39
        angle = 60
        size=13
    else:
        assert False,f"Get invalid terminal ion type {ion_type}"
    ion_trace = go.Scatter(x=[ion_trace_x],y=[ion_trace_y],
                            mode = 'markers',
                            name = None,
                            customdata=[ion_trace_x,ion_trace_y,angle,ion_type,the_mass,PCC,Error,Charge,Intensity,mz],
                            marker = dict(
                                symbol = 'line-ew',
                                color = color,
                                angle = angle,
                                size = size,
                                line = dict(
                                    color = color,
                                    width = 4)),
                            hovertemplate =  f'Observed Mass: {exp_mass}Da<br><br>'+
                                             f'Ion Type: {ion_type}<br>' +
                                             f'Theoretical Mass: {the_mass}Da<br>' +
                                             f'PCC: {PCC}<br>'+
                                             f'Error: {Error}ppm<br>'+f'Charge: {Charge}<br>'+f'Intensity: {Intensity}<br>'+f'mz: {mz}<br>')
    return ion_trace
#根据离子类型构建弯折图标
def terminal_ion_trace_contructor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)->go.Scatter:
    seg_trace_x,seg_trace_y = get_terminal_seg_trace_cor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)
    ion_trace = get_terminal_ion_trace(ions_df_i,seg_trace_x,seg_trace_y)
    return ion_trace
#输入一个离子，构建一个trace。弯折表示具体的离子类型，鼠标悬浮显示具体离子信息。
#该函数只生成终端离子的trace，内部离子另外生成，方便终端和内部离子分开展示
def terminal_seg_trace_constructor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)->go.Scatter:
    seg_trace_x,seg_trace_y = get_terminal_seg_trace_cor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)
    seg_trace = get_termimal_seg_trace(ions_df_i,seg_trace_x,seg_trace_y)
    return seg_trace

#按照角度大小将ion trace排序，优先角度大的trace，图层叠加会好看一些。
def post_process_ion_trace(ion_trace_list):
    return list(sorted(ion_trace_list,key=lambda x:x.marker.angle,reverse=True))

#按照离子类型对trace进行排序
def post_process_seg_trace(seg_trace_list):
    return list(sorted(seg_trace_list,key=lambda x:x.name,reverse=True))

#合并相同角度的离子trace
def merge_overlap_ion_trace(ion_trace_list):
    tmp_list = []
    #tmp_trace = go.Scatter()
    for trace in ion_trace_list:
        tmp_trace = copy.deepcopy(trace)
        for trace_2 in ion_trace_list:
            if trace is trace_2:
                pass
            else:
                if trace.customdata[0]==trace_2.customdata[0] and trace.customdata[1]==trace_2.customdata[1] and trace.customdata[2]==trace_2.customdata[2]:
                    ion_type = trace_2.customdata[3]
                    the_mass = trace_2.customdata[4]
                    PCC = trace_2.customdata[5]
                    Error = trace_2.customdata[6]
                    Charge = trace_2.customdata[7]
                    Intensity = trace_2.customdata[8]
                    mz = trace_2.customdata[9]
                    tmp_trace.hovertemplate += '<br>'+f'Ion Type: {ion_type}<br>' +f'Theoretical Mass: {the_mass}Da<br>' +f'PCC: {PCC}<br>'+f'Error: {Error}ppm<br>'+f'Charge: {Charge}<br>'+f'Intensity: {Intensity}<br>'+f'mz: {mz}<br>'
                #tmp_list.append[tmp_trace]
        tmp_trace.hovertemplate += '<extra></extra>'
        tmp_list.append(tmp_trace)
    return tmp_list

#根据序列长度计算fig的尺寸，193CA的是11x25刻度,对应像素为864x1679
def get_fig_size(x_cor_arr,y_cor_arr):
    heitght_px_ori=864
    width_px_ori=1679
    heitght_tick_ori=11
    width_tick_ori=25
    
    #不能按比例缩放，高度小于11个氨基酸时高度固定为864像素，大于时按照整倍增加
    height_fold = int(max(y_cor_arr)/heitght_tick_ori)+1#坐标从0开始，因此高度需要加1
    #width_tick = int(max(x_cor_arr)/width_px_ori)+1
    #print(height_tick)
    #print(width_tick)
    #一个刻度对应多少像素合适
    #heitght_tick_px = heitght_px_ori/heitght_tick_ori
    #width_tick_px = width_px_ori/width_tick_ori
    
    final_height_px = heitght_px_ori*height_fold
    final_width_px = width_px_ori
    #y轴刻度最大多少
    y_tick_limit = height_fold*heitght_tick_ori
    x_tick_limit = width_tick_ori
    return final_width_px,final_height_px,y_tick_limit,x_tick_limit

def seg_map_plot_main(workplace_dir,ions_df,seq):
    #获取每个氨基酸的笛卡尔坐标，在一象限显示
    seqLen = len(seq)
    x_cor_arr,y_cor_arr = get_seq_trace_cor(seq)
    fig_width,fig_height,y_tick_limit,x_tick_limit = get_fig_size(x_cor_arr,y_cor_arr)
    #print(fig_width)
    #print(fig_height)
    #隐藏坐标系和tick
    xaxis = go.layout.XAxis(ticks='', showticklabels=False, showline=False,range=[-1,x_tick_limit+1])
    yaxis = go.layout.YAxis(ticks='', showticklabels=False, showline=False,range=[-1,y_tick_limit])
    layout = go.Layout(template='simple_white',showlegend = False,xaxis = xaxis,yaxis = yaxis,height=fig_height,width=fig_width)
    #获取序列的trace，所有氨基酸都在一个trace
    seq_trace = get_seq_trace(seq,x_cor_arr,y_cor_arr)
    terminal_frag_df = get_terminal_frag_df(ions_df,seqLen)
    if not terminal_frag_df.empty:
        terminal_frag_df_PCC = terminal_frag_df[terminal_frag_df["adjust_PCC"]>=0.9]

        #获取每个碎裂位点的trace,每个位点单独一个trace，在相同位点产生的离子trace会重叠
        terminal_seg_site_trace = list(terminal_frag_df.apply(lambda x:terminal_seg_trace_constructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))
        terminal_seg_site_trace_PCC = list(terminal_frag_df_PCC.apply(lambda x:terminal_seg_trace_constructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))

        #按照离子类型反向排序
        terminal_seg_site_trace = post_process_seg_trace(terminal_seg_site_trace)
        terminal_seg_site_trace_PCC = post_process_seg_trace(terminal_seg_site_trace_PCC)

        #分离子类型的trace
        terminal_ion_site_trace = list(terminal_frag_df.apply(lambda x:terminal_ion_trace_contructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))
        terminal_ion_site_trace_PCC = list(terminal_frag_df_PCC.apply(lambda x:terminal_ion_trace_contructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))

        #按照弯折角度排序反向排序，大角度的trace再最低的图层
        terminal_ion_site_trace = post_process_ion_trace(terminal_ion_site_trace)
        terminal_ion_site_trace_PCC = post_process_ion_trace(terminal_ion_site_trace_PCC)

        #将重叠的trace的信息同步到表面的trace，方便显示信息。
        terminal_ion_site_trace = merge_overlap_ion_trace(terminal_ion_site_trace)
        terminal_ion_site_trace_PCC = merge_overlap_ion_trace(terminal_ion_site_trace_PCC)

        fig1 = go.Figure(terminal_seg_site_trace+terminal_ion_site_trace+[seq_trace],layout=layout)
        #不显示，仅保存
        plot(fig1, filename=fr"{workplace_dir}/terminal_seg_site_map.html", auto_open=False,include_plotlyjs=True)

        fig2 = go.Figure(terminal_seg_site_trace_PCC+terminal_ion_site_trace_PCC+[seq_trace],layout=layout)
        #不显示，仅保存
        plot(fig2, filename=fr"{workplace_dir}/terminal_seg_site_map_PCC.html", auto_open=False,include_plotlyjs=True)
    #fig.add_trace(seq_trace)
    #fig.show()
    internal_frag_df = get_internal_frag_df(ions_df,seqLen)
    if not internal_frag_df.empty:
        internal_seg_site_trace = list(internal_frag_df.apply(lambda x:internal_seg_trace_constructor(x,x_cor_arr,y_cor_arr),axis=1))
        #不显示，仅保存
        fig3 = go.Figure(internal_seg_site_trace+[seq_trace],layout=layout)
        plot(fig3,filename=fr"{workplace_dir}/internal_seg_site_map.html", auto_open=False,include_plotlyjs=True)

        #添加PCC>0.9的代码--zhuyl,230615
        internal_frag_df_PCC = internal_frag_df[internal_frag_df["adjust_PCC"]>=0.9]
        internal_seg_site_trace_PCC = list(internal_frag_df_PCC.apply(lambda x:internal_seg_trace_constructor(x,x_cor_arr,y_cor_arr),axis=1))
        #不显示，仅保存
        fig4 = go.Figure(internal_seg_site_trace_PCC+[seq_trace],layout=layout)
        plot(fig4,filename=fr"{workplace_dir}/internal_seg_site_map_PCC.html", auto_open=False,include_plotlyjs=True)
    
if __name__=="__main__":
    CA_seq = "SHHWGYGKHNGPEHWHKDFPIANGERQSPVDIDTKAVVQDPALKPLALVYGEATSRRMVNNGHSFNVEYDDSQDKAVLKDGPLTGTYRLVQFHFHWGSSDDQGSEHTVDRKKYAAELHLVHWNTKYGDFGTAAQQPDGLAVVGVFLKVGDANPALQKVLDALDSIKTKGKSTDFPNFDPGSLLPNVLDYWTYPGSLTTPPLLESVTWIVLKEPISVSSQQMLKFRTLNFNAEGEPELLMLANWRPAQPLKNRQVRGFPK"
    Ub_seq = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
    Mb_seq = "GLSDGEWQQVLNVWGKVEADIAGHGQEVLIRLFTGHPETLEKFDKFKHLKTEAEMKASEDLKKHGTVVLTALGGILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISDAIIHVLHSKHPGDFGADAQGAMTKALELFRNDIAAKYKELGFQG"
    M_apple_seq = "MVSKGEENNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEAFQTAKLKVTKGGPLPFAWDILSPQFMYGSKVYIKHPADIPDYFKLSFPEGFRWERVMNFEDGGIIHVNQDSSLQDGVFIYKVKLRGTNFPSDGPVMQKKTMGWEASEERMYPEDGALKSEIKKRLKLKDGGHYAAEVKTTYKAKKPVQLPGAYIVDIKLDIVSHNEDYTIVEQYERAEGRHSTGGMDELYKGSAFKLEHHHHHH"
    M_apple_67_AMF_seq = "VSKGEENNMAIIKEFMRFKVHMEGSVNGHEFEIEGEGEGRPYEAFQTAKLKVTKGGPLPFAWDILSPQFMYGSKVYIKHPADIPDYFKLSFPEGFRWERVMNFEDGGIIHVNQDSSLQDGVFIYKVKLRGTNFPSDGPVMQKKTMGWEASEERMYPEDGALKSEIKKRLKLKDGGHYAAEVKTTYKAKKPVQLPGAYIVDIKLDIVSHNEDYTIVEQYERAEGRHSTGGMDELYKGSAFKLEHHHHHH"
    
    NTerm_ion_type = ["x","x+1","x-1","y","y-2","z","z+1","z-1"]
    CTerm_ion_type = ["a","a+1","a-1","b","c","c."]
    internal_ion_type = ["ax","ay","az+2","bx","bz+2","cx","cy"]
    ion_type_color_map = {"red":["a","a+1","a-1","x","x+1","x-1"],"green":["b","y","y-1","y-2"],"blue":["c","c.","z","z+1","z-1"]}
    #msalign_dir= r"F:\JUPYTER\BPCR\DICP\ClipsMS\UE_output_230526\CA_shift"
    msalign_dir = r"F:\JUPYTER\BPCR\DICP\ClipsMS\UE_output_230616\M_Apple"
    #存放三个文件的文件夹名，该文件夹下包含mzml,msalign,raw这三个文件
    #msalign_filename= r"20220802_Native_Mb_193nm_Z8_SID15_3"
    #msalign_filename= r"20220411_NativeCA_UVPD193_Z10_AT1_3"
    #msalign_filename = "20230330_M_Apple_UVPD_193_1_5MJ_Z11_2591_4"
    msalign_filename = "20230607_APPLE_67_AMF_193nmUVPD_Z11_2579_4"
    test_seq = M_apple_67_AMF_seq
    seqLen = len(test_seq)
    input_dir = f"{msalign_dir}/{msalign_filename}"
    spec_num_i = 0
    #filename = "UE_output_s1.csv"
    #CA_output_s4 = get_CM_output(input_dir,spec_num_i,"UE_output_s4.csv")
    #CA_output_s2 = get_CM_output(input_dir,spec_num_i,"UE_output_s2.csv")
    CA_output_s1 = get_CM_output(input_dir,spec_num_i,"UE_output_s1.csv")
    seg_map_plot_main(input_dir,spec_num_i,CA_output_s1,test_seq)
