import argparse
from PandaUV_core import main,Param
import multiprocessing

def argp():
    paser=argparse.ArgumentParser(prog="Panda-UV",
                                  description="An efficient tool for high confident fragment assignment of UVPD data")

    paser.add_argument('-param_dir', help='Set the dir of param file required by Panda-UV', type=str, required=True)
    args = paser.parse_args()
    return args

if __name__=="__main__":
    multiprocessing.freeze_support()
    args = argp()
    param = Param()
    param.read_param(args.param_dir)
    main(param)
    main()

