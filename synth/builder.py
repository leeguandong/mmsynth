'''
@Time    : 2022/4/11 16:10
@Author  : leeguandon@gmail.com
'''
from .utils import build, Registry

RENDER = Registry('render')
DATASET = Registry('dataset')
MANAGER = Registry('manager')
CORPUS = Registry('corpus', parent=RENDER)
EFFECTS = Registry('effects')
LAYOUT = Registry('layout')


def build_dataset(cfg, default_args=None):
    return build(cfg, DATASET, default_args)


def build_render(cfg, default_args=None):
    return build(cfg, RENDER, default_args)


def build_corpus(cfg, default_args=None):
    return build(cfg, CORPUS, default_args)


def build_manager(cfg, default_args=None):
    return build(cfg, MANAGER, default_args)


def build_effects(cfg, default_args=None):
    return build(cfg, EFFECTS, default_args)


def build_layout(cfg, default_args=None):
    return build(cfg, LAYOUT, default_args)
