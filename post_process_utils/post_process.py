import pandas as pd
import numpy as np
from ion_match_utils.utils import get_CM_output,save_CM_output,get_terminal_frag_df,get_internal_frag_df
from post_process_utils import stratage_1,stratage_2,stratage_3,stratage_4
from seq_cov_utils.seq_cov_utils import get_seq_conv,get_matched_frags,get_terminal_seg_site,get_internal_seg_site
#返回离子匹配结果的数量，序列覆盖率，实验离子数量
def get_ions_num_and_cov(ions_df,seqLen):
    all_ions_num = len(ions_df)
    all_ions_cov = get_seq_conv(ions_df,seqLen)
    matched_frags_num = len(get_matched_frags(ions_df))
    return all_ions_num,all_ions_cov,matched_frags_num

#统计离子匹配结果
def sta_output(ions_df,seqLen):
    all_ions_num,all_ions_cov,all_matched_frags_num = get_ions_num_and_cov(ions_df,seqLen)

    terminal_ions_num,terminal_ions_cov,terminal_matched_frags_num = get_ions_num_and_cov(get_terminal_frag_df(ions_df,seqLen),seqLen)
    
    internal_ions_num,internal_ions_cov,internal_matched_frags_num = get_ions_num_and_cov(get_internal_frag_df(ions_df,seqLen),seqLen)
        
    return all_ions_num,all_ions_cov,all_matched_frags_num,terminal_ions_num,terminal_ions_cov,terminal_matched_frags_num,internal_ions_num,internal_ions_cov,internal_matched_frags_num

#获取离子匹配结果的统计信息的字符串，加上离子利用率的，zhuy--230529
def get_process_info(ions_df,mono_mass_arr,seqLen):
    all_num,all_cov,matched_frags_num,ter_num,ter_cov,ter_frags_num,int_num,int_cov,int_frags_num = sta_output(ions_df,seqLen)
    exp_ion_num = len(mono_mass_arr)#实验离子数量
    info_str = f"所有离子的数量：{all_num}\n所有离子的覆盖率：{all_cov}\n实验离子数量：{matched_frags_num}\n离子利用率：{matched_frags_num/exp_ion_num}\n\n终端离子的数量：{ter_num}\n终端离子的覆盖率：{ter_cov}\n实验离子数量：{ter_frags_num}\n离子利用率：{ter_frags_num/exp_ion_num}\n\n内部离子的数量：{int_num}\n内部离子的覆盖率：{int_cov}\n实验离子数量：{int_frags_num}\n离子利用率：{int_frags_num/exp_ion_num}"
    return info_str

def print_process_info(ions_df,mono_mass_arr,seqLen):
    print(get_process_info(ions_df,mono_mass_arr,seqLen))

#使用不同的策略进行处理，并保存结果。
def post_process_and_save(ions_df,mono_mass_arr,seqLen,workplace_dir,PCC_thr,Error_thr):
    UE_output_s1 = stratage_1.post_process(ions_df,seqLen,PCC_thr,Error_thr)
    UE_output_s1.to_csv(f"{workplace_dir}/UE_output_s1.csv",index=False)
    #save_CM_output(UE_output_s1,save_dir,spec_num_i,"UE_output_s1.csv")
    with open(f"{workplace_dir}/output_sta_s1.txt",mode="w") as f:
        f.write(get_process_info(UE_output_s1,mono_mass_arr,seqLen))#保存序列覆盖率等统计信息，zhuyl--230529
    
    UE_output_s2 = stratage_2.post_process(ions_df,seqLen,PCC_thr,Error_thr)
    UE_output_s2.to_csv(f"{workplace_dir}/UE_output_s2.csv",index=False)
    #save_CM_output(UE_output_s2,save_dir,spec_num_i,"UE_output_s2.csv")
    with open(f"{workplace_dir}/output_sta_s2.txt",mode="w") as f:
        f.write(get_process_info(UE_output_s2,mono_mass_arr,seqLen))
        
    UE_output_s3 = stratage_3.post_process(ions_df,seqLen,PCC_thr,Error_thr)
    UE_output_s3.to_csv(f"{workplace_dir}/UE_output_s3.csv",index=False)
    #save_CM_output(UE_output_s3,save_dir,spec_num_i,"UE_output_s3.csv")
    with open(f"{workplace_dir}/output_sta_s3.txt",mode="w") as f:
        f.write(get_process_info(UE_output_s3,mono_mass_arr,seqLen))
    
    UE_output_s4 = stratage_4.post_process(ions_df,seqLen,PCC_thr,Error_thr)
    UE_output_s4.to_csv(f"{workplace_dir}/UE_output_s4.csv",index=False)
    #save_CM_output(UE_output_s4,save_dir,spec_num_i,"UE_output_s4.csv")
    with open(f"{workplace_dir}/output_sta_s4.txt",mode="w") as f:
        f.write(get_process_info(UE_output_s4,mono_mass_arr,seqLen))

    
if __name__ == "__main__":
    CA_seq = "SHHWGYGKHNGPEHWHKDFPIANGERQSPVDIDTKAVVQDPALKPLALVYGEATSRRMVNNGHSFNVEYDDSQDKAVLKDGPLTGTYRLVQFHFHWGSSDDQGSEHTVDRKKYAAELHLVHWNTKYGDFGTAAQQPDGLAVVGVFLKVGDANPALQKVLDALDSIKTKGKSTDFPNFDPGSLLPNVLDYWTYPGSLTTPPLLESVTWIVLKEPISVSSQQMLKFRTLNFNAEGEPELLMLANWRPAQPLKNRQVRGFPK"
    Mb_seq = "GLSDGEWQQVLNVWGKVEADIAGHGQEVLIRLFTGHPETLEKFDKFKHLKTEAEMKASEDLKKHGTVVLTALGGILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISDAIIHVLHSKHPGDFGADAQGAMTKALELFRNDIAAKYKELGFQG"
    Ub_seq = "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG"
    Trastuzumab_seq = "DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC"
    
    msalign_dir = r"F:\JUPYTER\BPCR\DICP\ClipsMS\ClipsMS_output"
    msalign_filename = r"20220411_NativeCA_UVPD193_Z10_AT1_1"
    spec_num_i = 0
    test_seq = CA_seq
    seqLen = len(test_seq)
    input_dir = f"{msalign_dir}/{msalign_filename}"
    
    UE_output = get_CM_output(input_dir,spec_num_i,"Matched_Fragments_Final_scored_with_charge_and_PCC.csv")
    PCC_thr = 0.9
    Error_thr = 3
    post_process_and_save(UE_output,seqLen,input_dir,spec_num_i,PCC_thr,Error_thr)