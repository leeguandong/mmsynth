'''
@Time    : 2022/5/24 17:54
@Author  : leeguandon@gmail.com
'''
_base_ = [
    './_base_/default_runtime.py',
    './_base_/corpus/chn.py',
    './_base_/corpus/enum.py',
    './_base_/corpus/words.py',
    './_base_/corpus/rand.py',
    './_base_/layout.py',
    './_base_/effects.py'
]

bg = dict(
    type='BGManager',
    bg_dir="E:/comprehensive_library/mmsynth/data/bg",  # bg是jpg，代码中会转rgba，若是png，则保证alpha通道是255
    pre_load=True  # 将背景图加载到内存中
)
perspective_transform = dict(
    type='NormPerspectiveTransform',
    x=20,
    y=20,
    z=1.5,
    scale=1,
    fovy=50
)
enum_cropus = dict(
    type='EnumCorpus',
    items=['Hello! 你好！'],
    text_color=dict(
        type='ColorFixManager',
        color=(255, 50, 0, 255)
    ),
    font=dict(
        type='FontManager',
        font_dir='E:/comprehensive_library/mmsynth/data/fonts',
        font_list_file="E:/comprehensive_library/mmsynth/data/fonts_list/chn.txt",  # 要从font_dir中加载字体文件名，如果未提供，使用font_dir中所有字体
        font_size=(30, 31),  # 字体大小,本意是提供一个范围，这种写法其实就是固定了30
    )
)

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
    bg=bg,
    perspective_transform=perspective_transform,  # 作用在text_mask上
    return_bg_and_mask=False,  # 把文字和背景都返回
    name='render_chn',
)

render_rand = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.rand_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg,
    name='render_rand'
)

render_enum = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.enum_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg,
    name='render_enum'
)

render_eng = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.words_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg,
    name='render_eng'
)

same_line = dict(
    type='Render',
    gray=True,
    corpus=[{{_base_.chn_corpus}}, {{_base_.enum_corpus}}],
    corpus_effects=[  # 效果是作用在text_mask上的,一一对应，如果不佳效果就置空list
        [{{_base_.Line}}],
        [{{_base_.Padding}}]],
    layout={{_base_.SameLineLayout}},  # layout只在有多个语料时才设置，其实单语料也能设置
    layout_effects=[
        dict(
            type='Line',
            p=0.5,
            color=(255, 50, 0, 255)  # 线的颜色
        ),
    ],
    bg=bg,
    perspective_transform=perspective_transform,  # 作用在text_mask上
    return_bg_and_mask=False,  # 把文字和背景都返回
    name='same_line'
)

extra_text_line = dict(
    type='Render',
    corpus=[{{_base_.chn_corpus}}, {{_base_.chn_corpus}}],
    corpus_effects=[[{{_base_.Padding}}], []],
    layout={{_base_.ExtraTextLineLayout}},
    layout_effects=[
        dict(
            type='Line',
            p=1,
            color=(255, 50, 0, 255)  # 线的颜色
        ),
    ],
    bg=bg,
    perspective_transform=perspective_transform,  # 作用在text_mask上
    return_bg_and_mask=False,  # 把文字和背景都返回
    name='extra_text_line'
)

imgaug_emboss = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    corpus_effects=[{{_base_.Padding}}, {{_base_.Emboss}}],
    bg=bg,
    return_bg_and_mask=False,  # 把文字和背景都返回
    name='emboss'
)

curve = dict(
    type='Render',
    corpus=enum_cropus,
    corpus_effects=[{{_base_.Padding}}, {{_base_.Curve}}],
    bg=bg,
    return_bg_and_mask=False,  # 把文字和背景都返回
    name='curve'
)

vertical_text = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    bg=bg,
    name='vertical_text'
)

dropouthorizontal = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    corpus_effects=[{{_base_.DropoutHorizontal}}],
    bg=bg,
    name='dropouthorizontal'
)

bg_and_text_mask = dict(
    type='Render',
    height=48,  # 字体的高度限制
    corpus=enum_cropus,
    bg=bg,
    perspective_transform=dict(
        type='PerspectiveTransform',
        x=30,
        y=30,
        z=1.5,
        scale=1,
        fovy=50
    ),  # 作用在text_mask上
    return_bg_and_mask=True,  # 把文字和背景都返回
    name='bg_and_text_mask'
)

generator_cfg = [  # 配置多组不同形式的生成对象，同一组语料尽量配置多个生成组，效果更好
    render_chn,
    render_enum,
    render_eng,
    # render_rand,
    # same_line,
    # extra_text_line,
    # imgaug_emboss,
    # bg_and_text_mask,
    # curve,
    # vertical_text,
    dropouthorizontal
]
