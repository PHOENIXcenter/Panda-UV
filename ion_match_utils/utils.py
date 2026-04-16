###保存一些基本的读取文件和计算ppm的函数
import pandas as pd
import numpy as np
import copy
import os

#获取第spec_num_i个谱图文件夹下的csv文件
def get_CM_output(input_dir,spec_num_i,file_name):
    #file_name = "Matched_Fragments_Final_scored.csv"
    ions_df = pd.read_csv(f"{input_dir}/ms2_{spec_num_i}/{file_name}")
    return ions_df

#保存df到某个谱图的文件夹之下
#标准格式保存文件，如果文件夹不存在则创建文件夹--zhuyl,230525
def save_CM_output(df,save_dir,spec_num_i,file_name):
    output_dir = f"{save_dir}/ms2_{spec_num_i}"
    if os.path.exists(output_dir):
        pass
    else:
        os.makedirs(output_dir,exist_ok=True)
        print(f"Make dirs: {output_dir}")
    df.to_csv(f"{output_dir}/{file_name}",index=False)
    print("DataFrame saving successful. ")

#添加获取终端离子或者内部离子的函数，使用氨基酸长度获取--zhuyl,230516
def get_terminal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]==np.array([1,seqLen])
    return ions_df[np.any(flag_index,axis=1)]
def get_internal_frag_df(ions_df,seqLen):
    ions_df = copy.deepcopy(ions_df)
    flag_index = ions_df[["Start AA","End AA"]]!=np.array([1,seqLen])
    return ions_df[np.all(flag_index,axis=1)]

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
    #每个谱图前面都有一部分谱图相关信息，目前用不到，先去掉
    sprectra_info_length = 14
    mono_list = []
    for i in index_list:
        i_range = range(i[0]+sprectra_info_length,i[1])
        mono_list.append(fulltxt_list[i_range])
    #去除\t并构成numpy矩阵
    mono_arr = []
    for mono_list_i in mono_list:
        #print(mono_list[mono_list_i])
        mono_arr.append(np.asarray(list(map(lambda x:x.split("\t"),mono_list_i))).astype(float))
    #print(mono_arr)
    mono_arr = np.asarray(mono_arr,dtype="object")
    return mono_arr


#获取当前谱图所有单同位素峰质量，忽略谱图信息
#标准格式读取msalign文件--zhuyl,230525
def get_mono_mass_arr(input_dir):
    msalign_suffix = "msalign"
    file_type = "ms2"
    msalign_filename = os.path.basename(input_dir)
    msalign_file = f"{input_dir}/{msalign_filename}_{file_type}.{msalign_suffix}"
    
    fulltxt_list = read_mslign(msalign_file)

    StartIndex = np.argwhere(fulltxt_list=='BEGIN IONS')
    EndIndex = np.argwhere(fulltxt_list=='END IONS')
    assert len(StartIndex)==len(EndIndex),"Mslign file ion error."

    DeconvIonInfoRange = np.hstack([StartIndex,EndIndex])#[n,2],第一列是startIndex，注意BEGIN_IONS后面跟着14行谱图信息

    mono_arr = get_monoarr_from_startAndendIndex(DeconvIonInfoRange,fulltxt_list)
    return mono_arr

#标准格式从msalign读取单同位素质量
def get_mono_in_file(input_dir,spec_num_i,add_H):
    H_Ion_mass = 1.00782503207
    
    mono_arr = get_mono_mass_arr(input_dir)
    
    if add_H:
        #intensity比原始的大一个氢原子质量，不过影响不大。已修正
        #pd.DataFrame(mono_arr[spectrum_num][:,:2]+H_Ion_mass).to_csv(output_dir+"/"+output_filename,index=False)
        tmp_arr = copy.deepcopy(mono_arr[spec_num_i])
        #tmp_arr[:,0] += H_Ion_mass
        mz_arr = tmp_arr[:,0]/tmp_arr[:,2]+H_Ion_mass
        #改为计算单同位素峰的位置
        tmp_arr[:,0] += H_Ion_mass
        tmp_arr = np.hstack([tmp_arr,mz_arr[:,np.newaxis]])
        #pd.DataFrame(tmp_arr).to_csv(output_dir+"/"+output_filename,index=False)
        return pd.DataFrame(tmp_arr,columns = ["Mass","Intensity","Charge","mz"])
    else:
        #pd.DataFrame(mono_arr[spectrum_num][:,:2]).to_csv(output_dir+"/"+output_filename,index=False)
        tmp_arr = copy.deepcopy(mono_arr[spec_num_i])
        mz_arr = tmp_arr[:,0]/tmp_arr[:,2]+H_Ion_mass
        tmp_arr = np.hstack([tmp_arr,mz_arr[:,np.newaxis]])
        #pd.DataFrame(tmp_arr).to_csv(output_dir+"/"+output_filename,index=False)
        return pd.DataFrame(tmp_arr,columns = ["Mass","Intensity","Charge","mz"])
    #print(f"{msalign_filename}共{spectrum_num+1}张谱图保存完毕。")

#[M+H]+模式保存一个raw文件所有的谱图，用于ClipsMs输入。
#spec_num是msalign文件中存在的谱图的数量，使用该函数可一次性保存所有信息。
def save_mono_in_file(input_dir,spec_num,add_H):
    output_filename = "mono_mass_with_charge.csv"
    for spec_num_i in range(spec_num):
        mono_mass_df = get_mono_in_file(input_dir,spec_num_i,add_H)
        save_CM_output(mono_mass_df,input_dir,spec_num_i,output_filename)
    print(f"{input_dir}共{spec_num+1}张谱图保存完毕。")



#按照ppm计算
def mz_tolerance(mz,ppm):
    left = mz/(1+ppm/1e6)
    right = mz+mz*ppm/1e6
    return [left,right]

#计算两个值之间，向量之间，向量和值之间的误差。
def cal_ppm(mz1,mz2):
    ppm = ((mz1-mz2)/mz2)*1e6
    return ppm

#和cal_ppm相同的计算方式
def cal_mz(mz,ppm):
    left = mz/(1+ppm/1e6)
    return left