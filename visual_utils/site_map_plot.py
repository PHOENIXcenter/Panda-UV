import pandas as pd
import numpy as np
import os
import sys

import plotly
import plotly.graph_objs as go
from plotly.offline import plot

import math

import copy


from ion_match_utils.utils import get_CM_output,save_CM_output,get_terminal_frag_df,get_internal_frag_df

from seq_cov_utils.seq_cov_utils import get_seq_conv,get_matched_frags,get_terminal_seg_site,get_internal_seg_site,get_N_terminal_seg_site,get_C_terminal_seg_site
ion_type_color_map = {"red":["a","a+1","a-1","x","x+1","x-1"],"green":["b","y","y-1","y-2"],"blue":["c","c.","z","z+1","z-1"]}
def get_seq_trace_cor(seq)->[np.ndarray,np.ndarray]:
    width = 25
    high = 10
    seqLen = len(seq)
    real_high = int(seqLen/width)+1
    x_cor_arr = np.tile(np.arange(width),real_high)
    x_cor_arr = x_cor_arr[:seqLen]
    y_cor_arr = np.reshape(np.tile(np.array(list(reversed(np.arange(real_high)))),width),[width,real_high]).T
    y_cor_arr = np.reshape((y_cor_arr),[-1])
    y_cor_arr = y_cor_arr[:seqLen]
    
    return x_cor_arr,y_cor_arr

def get_seq_trace(seq,x_cor_arr,y_cor_arr)->go.Scatter:
    
    seq_list = ['<b>' + aa + '<b>' for aa in seq]
    seqLen = len(seq)
    site_num = list(np.arange(seqLen)+1)
    hovertext = [AA+str(site_num_i) for AA,site_num_i in zip(list(seq),site_num)]
    seq_trace = go.Scatter(x=x_cor_arr,y=y_cor_arr,
                                       mode="text",
                                       text=seq_list,
                                       textfont = dict(family = 'Arial', size = 40),
                                       textposition="middle center",
                                       hovertext=hovertext,
                                       hoverinfo="text")
    return seq_trace

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
def terminal_ion_trace_contructor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)->go.Scatter:
    seg_trace_x,seg_trace_y = get_terminal_seg_trace_cor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)
    ion_trace = get_terminal_ion_trace(ions_df_i,seg_trace_x,seg_trace_y)
    return ion_trace
def terminal_seg_trace_constructor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)->go.Scatter:
    seg_trace_x,seg_trace_y = get_terminal_seg_trace_cor(ions_df_i,seqLen,x_cor_arr,y_cor_arr)
    seg_trace = get_termimal_seg_trace(ions_df_i,seg_trace_x,seg_trace_y)
    return seg_trace

def post_process_ion_trace(ion_trace_list):
    return list(sorted(ion_trace_list,key=lambda x:x.marker.angle,reverse=True))

def post_process_seg_trace(seg_trace_list):
    return list(sorted(seg_trace_list,key=lambda x:x.name,reverse=True))

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

def get_fig_size(x_cor_arr,y_cor_arr):
    heitght_px_ori=864
    width_px_ori=1679
    heitght_tick_ori=11
    width_tick_ori=25
    
    height_fold = int(max(y_cor_arr)/heitght_tick_ori)+1
    
    final_height_px = heitght_px_ori*height_fold
    final_width_px = width_px_ori
    y_tick_limit = height_fold*heitght_tick_ori
    x_tick_limit = width_tick_ori
    return final_width_px,final_height_px,y_tick_limit,x_tick_limit

def seg_map_plot_main(workplace_dir,ions_df,seq):
    seqLen = len(seq)
    x_cor_arr,y_cor_arr = get_seq_trace_cor(seq)
    fig_width,fig_height,y_tick_limit,x_tick_limit = get_fig_size(x_cor_arr,y_cor_arr)
    xaxis = go.layout.XAxis(ticks='', showticklabels=False, showline=False,range=[-1,x_tick_limit+1])
    yaxis = go.layout.YAxis(ticks='', showticklabels=False, showline=False,range=[-1,y_tick_limit])
    layout = go.Layout(template='simple_white',showlegend = False,xaxis = xaxis,yaxis = yaxis,height=fig_height,width=fig_width)
    seq_trace = get_seq_trace(seq,x_cor_arr,y_cor_arr)
    terminal_frag_df = get_terminal_frag_df(ions_df,seqLen)
    if not terminal_frag_df.empty:
        terminal_seg_site_trace = list(terminal_frag_df.apply(lambda x:terminal_seg_trace_constructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))
        terminal_seg_site_trace = post_process_seg_trace(terminal_seg_site_trace)
        terminal_ion_site_trace = list(terminal_frag_df.apply(lambda x:terminal_ion_trace_contructor(x,seqLen,x_cor_arr,y_cor_arr),axis=1))
        terminal_ion_site_trace = post_process_ion_trace(terminal_ion_site_trace)
        terminal_ion_site_trace = merge_overlap_ion_trace(terminal_ion_site_trace)

        fig1 = go.Figure(terminal_seg_site_trace+terminal_ion_site_trace+[seq_trace],layout=layout)
        plot(fig1, filename=fr"{workplace_dir}/terminal_fragment_cleavage_map.html", auto_open=False,include_plotlyjs=True)

    internal_frag_df = get_internal_frag_df(ions_df,seqLen)
    if not internal_frag_df.empty:
        internal_seg_site_trace = list(internal_frag_df.apply(lambda x:internal_seg_trace_constructor(x,x_cor_arr,y_cor_arr),axis=1))
        fig3 = go.Figure(internal_seg_site_trace+[seq_trace],layout=layout)
        plot(fig3,filename=fr"{workplace_dir}/internal_fragment_cleavage_map.html", auto_open=False,include_plotlyjs=True)
