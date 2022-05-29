'''
@Time    : 2022/5/24 17:54
@Author  : leeguandon@gmail.com
'''
_base_ = [
    '../_base_/default_runtime.py',
    '../_base_/corpus/chn.py',
    '../_base_/effects.py'
]

render_chn = dict(  # 一组生成对象，
    type='Render',
    bg_dir="E:/comprehensive_library/mmsynth/data/bg",

    # perspective_transform='',
    gray=True,
    # layout='',
    # layout_effects='',
    corpus={{_base_.chn_corpus}},
    corpus_effects=[
        {{_base_.Line}},
        {{_base_.OneOf}}]
)

generator_cfg = [  # 配置多组不同形式的生成对象
    render_chn,
]
