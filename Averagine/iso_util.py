import sys
import os
from pyteomics import mass
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Averagine import averagine

avgDict = dict({'C':4.9384,'H':7.7583,'O':1.4773,'N':1.3577,'S':0.0417})
eleDict = dict({'C':12.00,'H':1.00782503207,'O':15.99491461956,'N':14.0030740048,'S':31.972071})
avgMass = 111.05430525080163
H_proton_mass = 1.00727646677

def mass_to_formula(_mass):
    avgUnit = _mass/avgMass
    avgFor = {}
    forStr = ""
    tmp_forStr = ""#如果出现元素数量小于0的情况，记录下该分子式
    offMass = 0
    for ele,num in avgDict.items():
        tmpUnit = num*avgUnit
        avgFor[ele] = round(tmpUnit)
        offUnit = tmpUnit - round(tmpUnit)
        offMass += eleDict[ele]*offUnit
    avgFor['H'] +=  round(offMass)
    for ele,num in avgFor.items():
        #如果出现负元素数，则将元素数设置为0，因为匹配理论和实验同位素分布会矫正--zhuyl, 2508230
        #设置警告提示哪些离子做了0设置
        if(num>0):
            forStr += str(ele)+str(num)
        if(num!=0):
            tmp_forStr += str(ele)+str(num)
    #if forStr!=tmp_forStr:
    #    print(f"Warning, formula {tmp_forStr} -> {forStr}")
    return forStr

def iso_adjust(_mass,charge,iso_peak_arr):
    offMz = iso_peak_arr[0,0] - (_mass/charge+H_proton_mass)
    iso_peak_arr[:,0] -= offMz
    return iso_peak_arr

def mass_to_iso(_mass,charge):
    iso_peak_arr = averagine.formula_to_iso(mass_to_formula(_mass),charge)
    iso_peak_arr = iso_adjust(_mass,charge,iso_peak_arr)
    return iso_peak_arr

if __name__ == "__main__":
    test_formula = 'H749C470O136N131S1'
    result1 = averagine.formula_to_iso(test_formula, 5)
    print(result1)
    result2 = averagine.mass_to_iso(mass.calculate_mass(test_formula), 5)
    print(result2)
    # 返回 shape=(N, 2) 的 numpy array
    # 每行 [mass, relative_abundance]
    test_mass = mass.calculate_mass(formula = test_formula,charge=0)
    result3 = mass_to_iso(test_mass,5)
    print(result3)