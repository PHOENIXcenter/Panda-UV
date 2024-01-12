#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load ProteinClass.py
#优化PANDA-UV核心代码--zhuyl,230816
#修复了蛋白质clip之后修饰loc不变的bug，现在clip之后的蛋白也可以正确显示修饰。


# In[1]:


from pyteomics import mass
import numpy as np
import copy

import re

_atom = r'([A-Z][a-z+]*)([+-]?\d+)?'
_formula = r'^({})*$'.format(_atom)


# In[32]:


#修饰类，可以通过+加入到蛋白质类的修饰列表中
#优化Mod类--zhuyl,230821
class Mod(object):
    
    def __init__(self,name,formula,loc,_mass):
        #self.mod_template = {}
        self.name = name
        #分子式自动整合
        self.formula = self.formula_init(formula)
        self.loc = loc
        #防止和pyteomics的mass模块冲突，加入_前缀，表示私有属性
        self.mass = _mass
        self.check_input()
    
    def __str__(self):
        out_str = f"Mod(name:{self.name},formula:{self.formula},location:{self.loc},mass:{self.mass})"
        return out_str
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self,mod):
        if mod.name == self.name and self.formula_init(mod.formula)==self.formula_init(self.formula) and mod.loc == self.loc and mod.mass == self.mass:
            return True
        else:
            return False
    
    #将字典类型的分子式转为str类型
    @staticmethod
    def comp_to_formula(formula_dict):
        tmp_s = ""
        for k,v in formula_dict.items():
            tmp_s += str(k)+str(v)
        return tmp_s
    
    #整合formula的格式
    @staticmethod
    def formula_init(formula):
        tmp_dict = {}
        for elem, number in re.findall(_atom, formula):
            if elem in tmp_dict.keys():
                tmp_dict[elem] += int(number) if number else 1
            else:
                tmp_dict[elem] = int(number) if number else 1
        return __class__.comp_to_formula(tmp_dict)

    def check_input(self):
        if not isinstance(self.formula,str):
            assert False,"Formula must be str. "
        
        if not isinstance(self.name,str):
            assert False,"Name must be str. "
            
        if not isinstance(self.loc,int):
            assert False,"Localzation must be intager. "
            
        if isinstance(self.mass,int) or isinstance(self.mass,float):
            pass
        else:
            assert False,"Mass must be intager or float. "


# In[35]:


#固定N端修饰的格式，添加了类属性和实例属性作为标识
class NTermMod(Mod):
    loc = 1
    def __init__(self,name,formula,_mass):
        loc = self.loc
        super().__init__(name,formula,loc,_mass)
        
        #self.check_input()
    def check_input(self):
        super().check_input()
        #检查终端修饰的格式是否正确
        
        assert self.name.endswith("-"),"N terminal modification name must end with '-'"
        assert self.name.islower(),"N terminal modification name must be lower alphabet"
        
class CTermMod(Mod):
    loc = -1
    def __init__(self,name,formula,_mass):
        loc = self.loc
        super().__init__(name,formula,loc,_mass)
        
        #self.check_input()
    def check_input(self):
        super().check_input()
        #检查终端修饰的格式是否正确
        #C端修饰需要检查是否-开头
        assert self.name.startswith("-"),"N terminal modification name must start with '-'"
        assert self.name.islower(),"N terminal modification name must be lower alphabet"
        


# In[60]:


#六种基础离子类型和mass.std_ion_comp["*"]的分子式一样
class AMod(CTermMod):
    name = "-a"
    formula = "H-2O-2C-1"
    _mass = -46.005479303259996
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)
        

class BMod(CTermMod):
    name = "-b"
    formula = "H-2O-1"
    _mass = -18.0105646837
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)

class CMod(CTermMod):
    name = "-c"
    formula = "H1O-1N1"
    _mass = -0.9840155826899988
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)

class C_dot_Mod(CTermMod):
    name = "-c_dot"
    formula = "H-4O-1N-1"
    _mass = -34.02928875264
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)
        
class XMod(NTermMod):
    name = "x-"
    formula = "H-2O1C1"
    _mass = 25.97926455542
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)

class YMod(NTermMod):
    name = "y-"
    formula = ""
    _mass = 0
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)

class ZMod(NTermMod):
    name = "z-"
    formula = "H-3N-1"
    _mass = -17.02654910101
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)

#C端得氢修饰
class C_HMod(CTermMod):
    name = "-hy"
    formula = "H"
    _mass = 1.00782503207
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)
#C端脱氢修饰
class C_H_loss_Mod(CTermMod):
    name = "-hy."
    formula = "H-1"
    _mass = -1.00782503207
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)
#N端得氢修饰
class N_HMod(NTermMod):
    name = "hy-"
    formula = "H"
    _mass = 1.00782503207
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)
#N端脱氢修饰
class N_H_loss_Mod(NTermMod):
    name = "hy.-"
    formula = "H-1"
    _mass = -1.00782503207
    def __init__(self):
        name = self.name
        formula = self.formula
        _mass = self._mass
        super().__init__(name,formula,_mass)


# In[61]:


class Protein(object):
    
    def __init__(self,seq):
        self.seq = seq
        #loc: [Mod]
        self.mod_list = {}
    #此处有一个bug，在Clip之后修饰会显示不出来
    #bug已修复,在Clip之后修饰的loc会改变，在显示时可以正确显示--zhuyl,230816
    def __str__(self):
        parsed_seq = ""
        seqLen = self.SEQLEN
        for i in range(1,seqLen+1):
            parsed_seq += self.seq[i-1]
            if i in self.mod_list.keys():
                parsed_seq += "("
                for mod in self.mod_list[i]:
                    parsed_seq += mod.name + "|"
                parsed_seq += ")"
                
        return parsed_seq
    
    def __repr__(self):
        return str(self)
    
    def __add__(self,mod):
        #后续会更改mod的属性，需要复制，防止被添加的mod的属性被改变
        mod = copy.deepcopy(mod)
        mod_loc = mod.loc
        assert abs(mod_loc)<=self.SEQLEN and mod_loc!=0,"Mod loc too large"
        protein = copy.deepcopy(self)
        #loc为负时，通过蛋白的长度映射到正确的loc
        if mod_loc<0:
            mod_loc = protein.SEQLEN + mod_loc + 1
            #更改Mod的loc，保持和mod_list的key一致。
            mod.loc = mod_loc
        else:
            pass
        if mod_loc in protein.mod_list.keys():
            protein.mod_list[mod_loc].append(mod)
        else:
            protein.mod_list[mod_loc] = [mod]
        return protein
    
    def __sub__(self,mod):
        #后续会更改mod的属性，需要复制，防止被添加的mod的属性被改变
        mod = copy.deepcopy(mod)
        mod_loc = mod.loc
        assert abs(mod_loc)<=self.SEQLEN and mod_loc!=0,"Mod loc too large"
        
        if mod_loc<0:
            mod_loc = self.SEQLEN + mod_loc + 1
            #更改Mod的loc，保持和mod_list的key一致。防止在减修饰时找不到对应修饰。
            mod.loc = mod_loc
        else:
            pass
        
        assert mod_loc in self.mod_list.keys(),"Mod loc wrong. "
        #print(mod)
        assert mod in self.mod_list[mod_loc],f"This AA has no mod {mod.name}. "
        
        protein = copy.deepcopy(self)
        
        for i in range(len(protein.mod_list[mod_loc])):
            #_mod = protein.mod_list[mod_loc][i]
            if mod == protein.mod_list[mod_loc][i]:
                del protein.mod_list[mod_loc][i]
                break
        if len(protein.mod_list[mod_loc]) == 0:
            del protein.mod_list[mod_loc]
        return protein
    
    
    @property
    def MASS(self):
        _mass = mass.fast_mass2(sequence=self.seq,charge=0)
        for loc,mod_list in self.mod_list.items():
            #if abs(loc)<=self.SEQLEN:，忽略修饰的位置，不管在哪里都计算质量--zhuyl,230517
            for mod in mod_list:
                _mass += mod.mass
        return _mass
    
    @property
    def SEQLEN(self):
        seqLen = len(self.seq)
        return seqLen
    
    @property
    def FORMULA(self):
        formula = self.comp_to_formula(mass.Composition(sequence = self.seq))
        for loc,mod_list in self.mod_list.items():
            #if abs(loc)<=self.SEQLEN:,忽略修饰的位置，不管在哪里都计算分子式--zhuyl,230517
            for mod in mod_list:
                formula += mod.formula
        formula = self.formula_init(formula)
        return formula
        
    @staticmethod
    def formula_init(formula):
        tmp_dict = {}
        for elem, number in re.findall(_atom, formula):
            if elem in tmp_dict.keys():
                tmp_dict[elem] += int(number) if number else 1
            else:
                tmp_dict[elem] = int(number) if number else 1
        return __class__.comp_to_formula(tmp_dict)
    
    @staticmethod
    def comp_to_formula(formula_dict):
        tmp_s = ""
        for k,v in formula_dict.items():
            tmp_s += str(k)+str(v)
        return tmp_s


# In[62]:


#碎裂为肽段，改变蛋白质序列和修饰
class Clip(object):
    def __init__(self,protein):
        
        self.protein = protein
        
    def clip(self,start,end):
        self.start = start
        self.end = end
        self.check_input()
        protein = copy.deepcopy(self.protein)
        
        del_mod_loc = []
        save_mod_loc = []
        for loc in protein.mod_list.keys():
            if loc>=start and loc<=end:
                save_mod_loc.append(loc)
                #pass
            else:
                del_mod_loc.append(loc)
        for loc in del_mod_loc:
            del protein.mod_list[loc]
        protein.seq = protein.seq[start-1:end]
        
        #for loc in save_mod_loc:
            
        #更新修饰的loc--zhuyl,230816
        new_mod_list = {}
        for loc in save_mod_loc:
            new_loc = loc-start+1
            new_mods = []
            for new_mod in protein.mod_list[loc]:
                new_mod.loc = new_loc
                new_mods.append(new_mod) 
            new_mod_list[new_loc] = new_mods
        protein.mod_list = new_mod_list
        return protein
    
    def __str__(self):
        return str(self.protein)
    
    def __repr__(self):
        return str(self.protein)
    
    def check_input(self):
        assert self.protein.__class__ is Protein,f"Protein must be {Protein}"
        assert isinstance(self.start,int) and isinstance(self.end,int),"Start and end index must be intager"
        seqLen = self.protein.SEQLEN
        assert self.start<=seqLen and self.end<=seqLen and self.start>0 and self.end>0,"Clip site must at AA"
        assert self.start<=self.end,"Clip start site must lt end site"
        


# In[63]:


class Ion(object):
    type_mod_dict = {"a":[AMod()],"b":[BMod()],"c":[CMod()],
                     "x":[XMod()],"y":[YMod()],"z":[ZMod()],
                     "a+1":[AMod() , C_HMod()] , "a-1":[AMod() , C_H_loss_Mod()],
                     "c-1":[CMod() , C_H_loss_Mod()],"c.":[C_dot_Mod()],
                     "x+1":[XMod() , N_HMod()],"x-1":[XMod() , N_H_loss_Mod()],
                     "y-1":[YMod() , N_H_loss_Mod()],"y-2":[YMod() , N_H_loss_Mod() , N_H_loss_Mod()],
                     "z+1":[ZMod() , N_HMod()],"z-1":[ZMod() , N_H_loss_Mod()],
                     "H":[N_HMod()],"-H":[N_H_loss_Mod()],
                     "ax":[XMod() , AMod() , N_HMod() , C_HMod()],"ay":[XMod() , BMod() , N_HMod() , C_HMod()],"az":[XMod() , CMod() , N_H_loss_Mod() , C_H_loss_Mod()],"az+1":[XMod() , CMod() , N_H_loss_Mod()],"az+2":[XMod() , CMod()],
                     "bx":[YMod() , AMod()],"by":[YMod() , BMod()],"bz":[YMod() , CMod() , N_H_loss_Mod() , C_H_loss_Mod() , N_H_loss_Mod() , C_H_loss_Mod()],"bz+2":[YMod() , CMod() , N_H_loss_Mod() , C_H_loss_Mod()],
                     "cx":[ZMod() , AMod() , N_HMod() , C_HMod()],"cy":[ZMod() , BMod() , N_HMod() , C_HMod()],"cz":[ZMod() , CMod() , N_H_loss_Mod() , C_H_loss_Mod()],"cz+2":[ZMod() , CMod()]}
    #valid_ion_type = type_mod_dict.keys()
    
    def __init__(self,protein):
        self.protein = protein
        self.protein.__class__ is Protein,f"Protein must be {Protein}"
        
    def ionization(self,ion_type):
        protein = copy.deepcopy(self.protein)
        #self.ion_type = ion_type
        ion_type in __class__.type_mod_dict.keys(),f"{ion_type} is an invalid ion type"
        for mod in __class__.type_mod_dict[ion_type]:
            protein += mod
        return protein
    
    #自定义离子类型，使用Mod类构建。一次可以添加多个修饰--zhuyl,230822
    @classmethod
    def add_ion_type(cls,type_name,*mods):
        if type_name in cls.type_mod_dict.keys():
            assert False,f"Ion type {type_name} exists. "
        else:
            cls.type_mod_dict[type_name] = list(mods)
    
    def __str__(self):
        return str(self.protein)
    
    def __repr__(self):
        return str(self.protein)
