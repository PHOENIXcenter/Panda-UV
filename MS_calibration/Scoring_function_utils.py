import pandas as pd
import numpy as np
from pyteomics import mass,mzml
import os
import copy

#计算两个值之间，向量之间，向量和值之间的误差。
def cal_ppm(mz1,mz2):
    ppm = ((mz1-mz2)/mz2)*1e6
    return ppm

#计算两个分布之间每个峰的距离--zhuyl,230824
def cal_d_mz(mz1,mz2):
    d_mz_arr = mz1-mz2
    return d_mz_arr
    
#根据ppm计算mz，和cal_ppm相同的计算方式
def cal_mz(mz,ppm):
    left = mz/(1+ppm/1e6)
    return left
    
#获取mzml文件某张谱的峰矩阵
def get_ms_peak_arr(mzml_file_dir,spec_num_i):
    ms_list = []
    with mzml.read(fr"{mzml_file_dir}") as mzfile:
    #auxiliary.print_tree(next(mzfile))
        for ms in mzfile:
            #print(ms)
            #break
            ms_list.append(ms)
    ms_i = ms_list[spec_num_i]
    ms_i_mz_arr = ms_i["m/z array"]
    ms_i_int_arr = ms_i["intensity array"]
    return np.stack([ms_i_mz_arr,ms_i_int_arr],axis=1)

#获取分布中最近的峰，不进行过滤
def get_closest_peak(iso_peak_arr,ms_peak_arr):
    match_peak_arr = np.zeros_like(iso_peak_arr,dtype=float)
    ms_peak_mz = ms_peak_arr[:,0]
    for i in range(len(iso_peak_arr)):
        iso_peak_i = iso_peak_arr[i]
        err_ppm = cal_ppm(ms_peak_mz,iso_peak_i[0])#这里计算的是实验和理论的偏差
        match_peak_index = np.argmin(abs(err_ppm))#这里一定要做绝对值
        match_peak = ms_peak_arr[match_peak_index]
        match_peak_arr[i] = match_peak
    return match_peak_arr

#根据化学式和电荷数获取理论同位素分布
def get_iso_peak_arr(r_source,chem_comp,charge):
    iso_df = r_source["FragIon.IsoPattern"](chem_comp,charge)
    iso_peak_arr = np.array(list(zip(list(iso_df[0]),list(iso_df[1]))),dtype=float)
    return iso_peak_arr

#根据分布计算PCC
def cal_PCC(iso_peak_arr,match_peak_arr):
    #if match_peak_arr[:,0]==0:
    #    return 0
    X = iso_peak_arr[:,1]
    Y = match_peak_arr[:,1]
    mean1 = np.mean(X)
    mean2 = np.mean(Y)
    tmp1 = X-mean1
    tmp2 = Y-mean2
    if np.all(tmp2)==0:#理论分布可能匹配不到实验分布，实验分布的mz 和 int全是0，造成0除错误。遇到这种情况直接全部范围0。
        return 0
    PCC = np.sum(tmp1*tmp2)/np.sqrt(np.sum(np.square(tmp1)))/np.sqrt(np.sum(np.square(tmp2)))
    return PCC

#使用ppm匹配实验同位素峰更准确
def iso_peak_match(iso_peak_arr,ms_peak_arr,peak_match_error):
    match_peak_arr = get_closest_peak(iso_peak_arr,ms_peak_arr)
    peak_err_arr = cal_ppm(match_peak_arr[:,0],iso_peak_arr[:,0])
    missing_peak_index = abs(peak_err_arr)>peak_match_error
    #将缺失峰的m/z设为对应理论峰的m/z
    match_peak_arr[:,0][missing_peak_index]=iso_peak_arr[:,0][missing_peak_index]
    #使用intensity==0的索引作为未匹配峰的标志--zhuyl,230913
    match_peak_arr[:,1][missing_peak_index]=0#超出ppm则认为没有匹配到峰，mz 和 int都设为0--zhuyl,230511
    return match_peak_arr

#返回根据err矫正之后的ms_i,输入mz_int_arr，默认not inplace
def mz_shift(ms_peak_arr,peak_shift_ppm):
    ms_peak_arr = copy.deepcopy(ms_peak_arr)
    ms_peak_arr[:,0] = cal_mz(ms_peak_arr[:,0],peak_shift_ppm)
    return ms_peak_arr

#对理论峰进行缩放
#改为按照强度前3的峰进行缩放
#有效峰数量小于3则使用所有的峰进行缩放
#强度前三的理论峰和对应的三个实验峰进行缩放,只考虑匹配上的峰，如果考虑填充峰会使整个峰型不符--zhuyl,230912
def peak_scale(iso_peak_arr,match_peak_arr):
    iso_peak_arr = copy.deepcopy(iso_peak_arr)
    matched_peak_index = match_peak_arr[:,1]!=0
    matched_peak_number = sum(matched_peak_index)
    yr_arr = copy.deepcopy(iso_peak_arr[:,1][matched_peak_index])
    y_dot_arr = copy.deepcopy(match_peak_arr[:,1][matched_peak_index])
    #获取理论峰最高三个峰的索引
    if matched_peak_number>=3:
        yr_h_top_three = np.sort(yr_arr)[-3]
        yr_h_top_three_index = yr_arr>=yr_h_top_three
        scale_factor = np.sum(y_dot_arr[yr_h_top_three_index])/np.sum(yr_arr[yr_h_top_three_index])
    elif matched_peak_number==0:
        scale_factor = 1
    else:
        scale_factor = np.sum(y_dot_arr)/np.sum(yr_arr)
    iso_peak_arr[:,1] *= scale_factor
    return iso_peak_arr

#根据L-Score的方法矫正实验同位素峰，只矫正匹配上的峰
#矫正所有的峰，包括强度为0的峰--zhuyl,230913
def peak_adjust(iso_peak_arr_scaled,match_peak_arr):
    match_peak_arr = copy.deepcopy(match_peak_arr)
    #筛选强度>0的峰作为匹配上的峰
    #matched_peak_index = match_peak_arr[:,1]!=0
    #计算匹配上的峰的数量
    #matched_peak_number = sum(matched_peak_index)
    #如果没有实验峰被匹配上
    #if matched_peak_number==0:
    #    return match_peak_arr
    #强度大于0的谱峰的强度向量
    #理论同位素峰的强度已经根据强度前三的峰等比例缩放过
    y_arr = copy.deepcopy(iso_peak_arr_scaled[:,1])
    y_dot_arr = copy.deepcopy(match_peak_arr[:,1])
    #匹配上的峰的叠加峰索引
    #overlap_index = y_dot_arr>y_arr
    #匹配上的峰的未叠加峰索引
    #normal_index = y_dot_arr<=y_arr
    
    #强度差阈值
    t = 0.5
    #惩罚项
    c = 1
    
    #打分使用相对强度进行打分
    #try:
    #缩放后的理论峰的最高强度峰的强度
    yh_index = np.argmax(y_arr)
    yh = y_arr[yh_index]
    #缩放为相对强度
    yr_arr = y_arr/yh
    #缩放后的实验峰的最高强度峰的强度
    yh_dot = yh
    #缩放为相对强度
    yr_dot_arr = y_dot_arr/yh_dot
    
    yr_dot_calibration = np.zeros_like(y_dot_arr)
    for i in range(len(y_dot_arr)):
        y = y_arr[i]
        y_dot = y_dot_arr[i]
        yr = yr_arr[i]
        yr_dot = yr_dot_arr[i]
        if y_dot>y:
            if abs(yr_dot-yr)<=t:
                yr_dot_calibration[i] = yr_dot
            else:
                if yr_dot>yr:
                    yr_dot_calibration[i] = yr+t
                else:
                    yr_dot_calibration[i] = yr-t
        else:
            if abs(yr_dot-yr)<=t:
                yr_dot_calibration[i] = yr+c*(yr_dot-yr)
            else:
                if yr_dot>yr:
                    yr_dot_calibration[i] = yr+c*t
                else:
                    yr_dot_calibration[i] = yr-c*t
    #yr_dot_calibration[yr_dot_calibration<0] = 0.01
    match_peak_arr[:,1] = yr_dot_calibration*yh_dot
    return match_peak_arr

#计算L-Score的距离打分部分
#m/z距离打分需要使用匹配上的峰--zhuyl,230913
def cal_dx(iso_peak_arr,match_peak_arr,peak_match_error):
    #只使用匹配上的峰计算
    matched_peak_index = match_peak_arr[:,1]!=0
    matched_peak_number = sum(matched_peak_index)
    x_arr = copy.deepcopy(iso_peak_arr[:,0][matched_peak_index])
    x_dot_arr = copy.deepcopy(match_peak_arr[:,0][matched_peak_index])
    #如果没有峰被匹配上,距离全都设置为10ppm
    if matched_peak_number==0:
        dx = np.sqrt(np.sum(np.square(x_arr-cal_mz(x_arr,peak_match_error)))/len(iso_peak_arr))
    else:
        dx = np.sqrt(np.sum(np.square(x_arr-x_dot_arr))/matched_peak_number)
    return dx

#计算实验谱峰的缺失峰数量，强度为0则认为是缺失谱峰
def cal_missing_peak_num(match_peak_arr):
    missing_peak_index = match_peak_arr[:,1] == 0
    missing_peak_number = sum(missing_peak_index)
    return missing_peak_number

#计算强度距离时使用所有的峰
def cal_dy_validation(iso_peak_arr_scaled,match_peak_arr_adjust):
    #matched_peak_index = match_peak_arr_adjust[:,0]!=0
    #matched_peak_number = sum(matched_peak_index)
    #if matched_peak_number==0:
    #    dy = np.sqrt(np.sum(np.square(iso_peak_arr_scaled[:,1]))/len(iso_peak_arr_scaled))
    y_arr = copy.deepcopy(iso_peak_arr_scaled[:,1])
    y_dot_arr = copy.deepcopy(match_peak_arr_adjust[:,1])
    #缩放后的理论峰的最高强度峰的强度
    yh_index = np.argmax(y_arr)
    yh = y_arr[yh_index]
    #缩放为相对强度
    yr_arr = y_arr/yh
    #缩放后的实验峰的最高强度峰的强度
    yh_dot = yh
    #缩放为相对强度
    yr_dot_arr = y_dot_arr/yh_dot
    
    dy_arr = yr_dot_arr-yr_arr
    dy = np.sqrt(np.sum(np.square(dy_arr))/len(y_dot_arr))
    return dy

#计算实验分布和理论分布强度的距离
#使用所有的峰计算距离--zhuyl,230913
def cal_dy(iso_peak_arr_scaled,match_peak_arr):
    #只使用强度大于0的峰计算
    #matched_peak_index = match_peak_arr[:,1]!=0
    #matched_peak_number = sum(matched_peak_index)
    #如果没有匹配上实验峰，则计算和0之间的距离
    #if matched_peak_number==0:
    #    dy = np.sqrt(np.sum(np.square(iso_peak_arr_scaled[:,1]))/len(iso_peak_arr_scaled))
    #return dy
    #需要输入缩放之后的理论同位素分布，使用绝对强度值进行比较
    y_arr = copy.deepcopy(iso_peak_arr_scaled[:,1])
    y_dot_arr = copy.deepcopy(match_peak_arr[:,1])
    #缩放后的理论峰的最高强度峰的强度
    #缩放后的理论峰的最高强度峰的强度
    yh_index = np.argmax(y_arr)
    yh = y_arr[yh_index]
    #缩放为相对强度
    yr_arr = y_arr/yh
    #缩放后的实验峰的最高强度峰的强度
    yh_dot = yh
    #缩放为相对强度
    yr_dot_arr = y_dot_arr/yh_dot

    #比较强度需要使用绝对强度
    overlap_index = y_dot_arr>y_arr
    normal_index = y_dot_arr<=y_arr
    #强度差阈值
    t = 0.5
    #惩罚项
    c = 2
    dy_arr = np.zeros_like(y_arr)
    if sum(overlap_index) >= 1:
        dy_arr[overlap_index] = np.min(np.vstack([abs(yr_arr[overlap_index]-yr_dot_arr[overlap_index]),np.array([t]*sum(overlap_index))]),axis=0)
    if sum(normal_index) >= 1:
        dy_arr[normal_index] = c*np.min(np.vstack([abs(yr_arr[normal_index]-yr_dot_arr[normal_index]),np.array([t]*sum(normal_index))]),axis=0)
    dy = np.sqrt(np.sum(np.square(dy_arr))/len(dy_arr))
    return dy

#CM的formula转为enviPat格式，元素个数不能为0
def comp_to_formula(s):
    formula = "".join(s.split(" "))
    formula_dict = mass.Composition(formula=formula)
    tmp_s = ""
    for k,v in formula_dict.items():
        tmp_s += str(k)+str(v)
    return tmp_s

#输入偏移之后的ms_mz_int_arr，和每一列ions_df,r函数对象，输出PCC,dx,dy,missing_peak_num四个打分项。
def get_score_term(ms_peak_arr_shift,ions_df_i,r_source,peak_match_error):
    #print(ions_df_i)
    formula = comp_to_formula(ions_df_i["Formula"])
    charge = int(ions_df_i["Charge"])
    #根据分子式和电荷计算理论同位素分布
    iso_peak_arr = get_iso_peak_arr(r_source,formula,charge)
    #根据理论同位素峰分布匹配实验分布，没有匹配到则使用对应的理论峰填充，强度设为0
    match_peak_arr = iso_peak_match(iso_peak_arr,ms_peak_arr_shift,peak_match_error)#误差距离超出ppm会变为0，表示没有匹配到峰
    #按照强度前3的理论峰对应的实验峰强度和的比值对理论分布进行缩放，只使用匹配上的峰。
    iso_peak_arr_scaled = peak_scale(iso_peak_arr,match_peak_arr)
    #对实验同位素峰强度进行矫正，包括强度为0的峰也进行矫正
    match_peak_arr_adjust = peak_adjust(iso_peak_arr_scaled,match_peak_arr)
    #except ValueError:
    #    print(ions_df_i)
    #计算PCC不需要对强度进行缩放，是否缩放对PCC打分没有影响
    PCC = round(cal_PCC(iso_peak_arr,match_peak_arr),4)
    adjust_PCC = round(cal_PCC(iso_peak_arr_scaled,match_peak_arr_adjust),4)
    dx = round(cal_dx(iso_peak_arr,match_peak_arr,peak_match_error),4)
    #使用所有的峰计算强度距离
    dy = round(cal_dy(iso_peak_arr_scaled,match_peak_arr),4)
    #dy_validation = round(cal_dy_validation(iso_peak_arr_scaled,match_peak_arr_adjust),4)
    #if dy!=dy_validation:
    #    print(f"dy err. {dy} and {dy_validation}")
    #    print(f"{formula}")
    #assert ,print(f"{formula}")
    peak_num = len(iso_peak_arr)
    missing_peak_num = cal_missing_peak_num(match_peak_arr)
    return [PCC,adjust_PCC,dx,dy,peak_num,missing_peak_num]