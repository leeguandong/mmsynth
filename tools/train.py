'''
@Time    : 2022/5/23 17:25
@Author  : leeguandon@gmail.com
'''
import copy
import random
import time
import argparse
import mmcv
import numpy as np
import os.path as osp

from mmcv import Config
from loguru import logger
from synth.api import train_data

work_dir = '../results'
logger.add(osp.join(work_dir, osp.basename(work_dir) + '.log'))


def parse_args():
    parser = argparse.ArgumentParser(description="features")
    parser.add_argument('--config', default="../configs/example.py",
                        help='train config file path')
    parser.add_argument('--work-dir', default=f"{work_dir}", help='the dir to save logs and models')
    parser.add_argument('--seed', type=int, default=2022, help='random seed')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cfg = Config.fromfile(args.config)
    cfg.merge_from_dict({"work_dir": args.work_dir})

    if args.work_dir is not None:
        # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs',
                                osp.splitext(osp.basename(args.config))[0])
        # create work_dir
    mmcv.mkdir_or_exist(osp.abspath(cfg.work_dir))
    # dump config
    cfg.dump(osp.join(cfg.work_dir, osp.basename(args.config)))
    # init the logger before other steps
    logger.info(f'Config:\n{cfg.pretty_text}')

    train_data(cfg)


if __name__ == "__main__":
    main()
