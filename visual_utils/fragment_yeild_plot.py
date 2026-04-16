import plotly.graph_objs as go
import pandas as pd

from plotly.offline import plot

import plotly.express as px

import numpy as np

import sys

import copy


from ion_match_utils.utils import get_CM_output,save_CM_output,get_terminal_frag_df,get_internal_frag_df

def get_TIC(ions_df)->float:
    return np.sum(ions_df["Intensity"])

def get_terminal_relative_AA_site(ions_df,seqLen)->pd.Series:
    AA_site_series = pd.Series(0,index=ions_df.index)
    N_ions_df = ions_df[ions_df["Start AA"]==1]
    C_ions_df = ions_df[ions_df["End AA"]==seqLen]
    AA_site_series[N_ions_df.index] = N_ions_df["End AA"]
    AA_site_series[C_ions_df.index] = C_ions_df["Start AA"]-1
    return AA_site_series

def get_terminal_abundance_fig(ions_df,seqLen):
    fig = px.bar(ions_df, x="Backbone position", y="Intensity", color="Frag Type")
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

def split_internal_to_terminal(internal_ions_df_i,seqLen):
    ion_type = internal_ions_df_i["Frag Type"]
    C_ion_type = ion_type[0]
    N_ion_type = ion_type[1]
    C_ions_df_i = copy.deepcopy(internal_ions_df_i)
    N_ions_df_i = copy.deepcopy(internal_ions_df_i)
    C_ions_df_i["Frag Type"] = C_ion_type
    C_ions_df_i["End AA"] = internal_ions_df_i["Start AA"]-1
    C_ions_df_i["Start AA"] = 1
    N_ions_df_i["Frag Type"] = N_ion_type
    N_ions_df_i["Start AA"] = internal_ions_df_i["End AA"]+1
    N_ions_df_i["End AA"] = seqLen
    return C_ions_df_i,N_ions_df_i

def fragment_abundance_plot_main(workplace_dir,ions_df,seq):
    seqLen = len(seq)
    terminal_frag_df = get_terminal_frag_df(ions_df,seqLen).sort_values("Frag Type")
    if not terminal_frag_df.empty:
        #terminal_frag_df_PCC = copy.deepcopy(terminal_frag_df[terminal_frag_df["adjust_PCC"]>=0.6]).sort_values("Frag Type")
        terminal_relative_AA_site = get_terminal_relative_AA_site(terminal_frag_df,seqLen)
        #terminal_relative_AA_site_PCC = get_terminal_relative_AA_site(terminal_frag_df_PCC,seqLen)
        terminal_frag_df["Backbone position"] = terminal_relative_AA_site
        #terminal_frag_df_PCC["Backbone position"] = terminal_relative_AA_site_PCC

        termianl_abundance_fig = get_terminal_abundance_fig(terminal_frag_df,seqLen)
        #termianl_abundance_fig_PCC = get_terminal_abundance_fig(terminal_frag_df_PCC,seqLen)

        plot(termianl_abundance_fig,filename=fr"{workplace_dir}/bar_plot_of_terminal_residual_fragment_yield.html", auto_open=False,include_plotlyjs=True)
        #plot(termianl_abundance_fig_PCC,filename=fr"{workplace_dir}/terminal_abundance_map_PCC.html", auto_open=False,include_plotlyjs=True)
    
    internal_frag_df = get_internal_frag_df(ions_df,seqLen)
    if not internal_frag_df.empty:
        split_internal_df = pd.DataFrame(columns=internal_frag_df.columns)
        for _,internal_frag_df_i in internal_frag_df.iterrows():
            split_internal_df_i_1,split_internal_df_i_2 = split_internal_to_terminal(internal_frag_df_i,seqLen)
            split_internal_df = split_internal_df.append([split_internal_df_i_1,split_internal_df_i_2])
        split_internal_df.reset_index(inplace=True)
        internal_relative_AA_site = get_terminal_relative_AA_site(split_internal_df,seqLen)
        split_internal_df["Backbone position"] = internal_relative_AA_site
        #split_internal_df_PCC = split_internal_df[split_internal_df["adjust_PCC"]>=0.8]
        internal_abundance_fig = get_terminal_abundance_fig(split_internal_df.sort_values("Frag Type"),seqLen)
        #internal_abundance_fig_PCC = get_terminal_abundance_fig(split_internal_df_PCC.sort_values("Frag Type"),seqLen)
        plot(internal_abundance_fig,filename=fr"{workplace_dir}/bar_plot_of_internal_residual_fragment_yield.html", auto_open=False,include_plotlyjs=True)
        #plot(internal_abundance_fig_PCC,filename=fr"{workplace_dir}/internal_abundance_map_PCC.html", auto_open=False,include_plotlyjs=True)    