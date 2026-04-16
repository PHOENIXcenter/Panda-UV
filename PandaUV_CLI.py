import argparse
from PandaUV_core import main
import multiprocessing

def argp():
    paser=argparse.ArgumentParser(prog="PANDA-UV",
                                  description="An efficient tool for high confident fragment assignment of UVPD data")

    paser.add_argument('-param_dir', help='Set the dir of param file required by Panda-UV', type=str, required=True)
    #paser.add_argument('-fixed_mod_dir', help='蛋白的修饰文件路径', type=str, required=False)
    args = paser.parse_args()
    return args

if __name__=="__main__":
    multiprocessing.freeze_support()
    args = argp()
    main(args.param_dir)

