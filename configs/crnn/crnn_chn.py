'''
@Time    : 2022/5/24 17:54
@Author  : leeguandon@gmail.com
'''
_base_ = [
    '../_base_/default_runtime.py',
    '../_base_/corpus/chn.py',
    '../_base_/corpus/enum.py',
    '../_base_/effects.py'
]

render_chn = dict(  # 一组生成对象，
    type='Render',
    height=32,  # 字体的高度限制
    render_effects=[{{_base_.Line}}],  # 作用在合成的图上,bg+text_mask
    gray=True,
    corpus={{_base_.chn_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    corpus_effects=[  # 效果是作用在text_mask上的
        {{_base_.Line}},
        {{_base_.Padding}}],
    # layout='',  # layout只在有多个语料时才设置，其实单语料也能设置
    # layout_effects='',
    bg=dict(
        type='BGManager',
        bg_dir="E:/comprehensive_library/mmsynth/data/bg",  # bg是jpg，代码中会转rgba，若是png，则保证alpha通道是255
        pre_load=True  # 将背景图加载到内存中
    ),
    perspective_transform=dict(
        type='NormPerspectiveTransform',
        x=20,
        y=20,
        z=1.5,
        scale=1,
        fovy=50
    ),  # 作用在text_mask上
    return_bg_and_mask=True  # 把文字和背景都返回
)

same_line = dict(
    type='Render',
    gray=True,
    corpus=[{{_base_.chn_corpus}}, {{_base_.enum_corpus}}],
    corpus_effects=[  # 效果是作用在text_mask上的,一一对应，如果不佳效果就置空list
        [{{_base_.Line}}],
        [{{_base_.Padding}}]],
    layout=dict(
        type='SameLineLayout',
        h_spacing=(0, 1),
    ),  # layout只在有多个语料时才设置，其实单语料也能设置
    layout_effects=[
        dict(
            type='Line',
            p=0.5,
            color=(255, 50, 0, 255)  # 线的颜色
        ),
    ],
    bg=dict(
        type='BGManager',
        bg_dir="E:/comprehensive_library/mmsynth/data/bg",  # bg是jpg，代码中会转rgba，若是png，则保证alpha通道是255
        pre_load=True  # 将背景图加载到内存中
    ),
    perspective_transform=dict(
        type='NormPerspectiveTransform',
        x=20,
        y=20,
        z=1.5,
        scale=1,
        fovy=50
    ),  # 作用在text_mask上
    return_bg_and_mask=True  # 把文字和背景都返回
)

generator_cfg = [  # 配置多组不同形式的生成对象，同一组语料尽量配置多个生成组，效果更好
    # render_chn,
    same_line,
]
