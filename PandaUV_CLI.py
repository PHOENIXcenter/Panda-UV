#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
from PandaUV_main import main


# In[2]:


def argp():
    paser=argparse.ArgumentParser(prog="PANDA-UV 1.0",
                                  description="An efficient tool for high confident fragment assignment of UVPD data")

    paser.add_argument('-param_dir', help='Set the dir of param file reqired by Panda-UV', type=str, required=True)
    #paser.add_argument('-fixed_mod_dir', help='蛋白的修饰文件路径', type=str, required=False)
    args = paser.parse_args()
    return args


# In[3]:


if __name__=="__main__":
    args = argp()
    main(args.param_dir)

