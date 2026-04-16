import re
import numpy as np
import pandas as pd

def msAlignParse(ion_text_list):
    infoDict = {}
    infoDict["mono_arr"]=np.array([])
    mono_arr = []
    for text in ion_text_list:
        if re.search("=",text):
            key,value = text.split("=")
            infoDict[key]=value
        else:
            mono_arr.append(text.split("\t"))
    #print(mono_arr)
    #如果谱图没有去卷积结果则打印提示信息
    if len(mono_arr):
        infoDict["mono_arr"]=np.vstack(np.array(mono_arr,dtype=float))
    else:
        scans = infoDict["SCANS"]
        print(f"Scan {scans} has no deconvoluted ions")
    return infoDict

#将mslign文件每行都读入一个列表
def read_mslign(file_name):
    file = open(file_name)
    fulltxt = file.read()
    fulltxt_list = fulltxt.split("\n")
    file.close()
    return np.asarray(fulltxt_list)

#从msalign文件获取谱图所有的离子，按照谱图顺序排列
#输出一个[n,m,3]的array,n是谱图数，m是每个谱图的离子数量，3分别是mass,intensity，charge state
#startIndex和endIndex从fulltxt_list切片得到相应的单同位素矩阵
def get_monoarr_from_startAndendIndex(index_list,fulltxt_list):
    mono_list = []#此处换成np，并提前设好形状，后面替换数据可能会更快一些
    for i in index_list:
        i_range = range(i[0],i[1])
        mono_list.append(fulltxt_list[i_range])
    #去除\t并构成numpy矩阵
    deconv_info = []
    for mono_list_i in mono_list:
        deconv_info.append(msAlignParse(mono_list_i))
        #break
    #print(mono_arr)
    return deconv_info

def dec_res_to_str(dec_mass,mass_int,mono_charge):
    sort_index = np.argsort(dec_mass)
    dec_mass = dec_mass[sort_index].round(5).astype(str)
    mass_int = mass_int[sort_index].round(2).astype(str)
    mono_charge = mono_charge[sort_index].round().astype(str)
    return dec_mass,mass_int,mono_charge

def to_csv_string(arr, sep='\t', lineterminator='\n'):
    lines = [sep.join(str(x) for x in row) for row in arr]
    return lineterminator.join(lines)

def dec_info_to_msalign_str(dec_info):
    head_info = "BEGIN IONS\n"
    dec_info_suf = "\nEND IONS\n"

    for key,value in dec_info.items():
        if key!="mono_arr":
            head_info += f"{key}={value}\n"
        else:
            dec_mass = dec_info["mono_arr"][:,0]
            mass_int = dec_info["mono_arr"][:,1]
            mono_charge = dec_info["mono_arr"][:,2].astype(int)
            dec_mass,mass_int,mono_charge = dec_res_to_str(dec_mass,mass_int,mono_charge)
            dec_str = to_csv_string(np.stack([dec_mass, mass_int, mono_charge], axis=1))

    msalign_str = head_info+dec_str+dec_info_suf
    return msalign_str

#获取当前谱图所有单同位素峰质量，忽略谱图信息
#输入的是msalign的路径
def get_dec_info(msalign_file_dir):
    
    fulltxt_list = read_mslign(msalign_file_dir)

    StartIndex = np.argwhere(fulltxt_list=='BEGIN IONS')+1
    EndIndex = np.argwhere(fulltxt_list=='END IONS')
    assert len(StartIndex)==len(EndIndex),"Mslign file ion error."

    DeconvIonInfoRange = np.hstack([StartIndex,EndIndex])#[n,2],第一列是startIndex，注意BEGIN_IONS后面跟着14行谱图信息

    mono_arr = get_monoarr_from_startAndendIndex(DeconvIonInfoRange,fulltxt_list)
    return mono_arr

if __name__ == "__main__":
    test_msalign_path = "20200110_ubiquitin_193nm_1_2mj_monomer_Z6_1428_1_ms2.msalign"
    test_dec_info = get_dec_info(test_msalign_path)
    test_msalign_str = dec_info_to_msalign_str(test_dec_info[0])
    with open(f"test_ms2.msalign","w") as f:
        f.write(test_msalign_str)
    pass