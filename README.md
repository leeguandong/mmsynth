# mmsynth
这个库的主要目的是合成数据，不是数据增强（在线数据增强和离线数据增强应该比较相似，除非在batch梯度上有操作，否则应该都差不多），
期望是应用在两个维度，一个是文本字符数据集的生成，即crnn的数据，一个ps篡改数据生成。数据合成在很多情况下是解决视觉算法问题的重要手段。

## 主要特性
 - [x] 模块化设计，主要包括corpus/effects/layout和models模块，其中corpus是语料类，包括char/enum/rand/word
 - [x] 丰富的特效，集成了[imgaug](https://github.com/aleju/imgaug)
 - [x] 支持在合成图的不同阶段使用特效，一般是text_mask阶段和合成图阶段
 - [x] 支持横竖文本生成
 - [x] 在设计上保证了config的纯粹性，隔离模块和config，不在config中做初始化等操作
 - [x] 对齐mm系列代码

## 文本输出
The data is generated in the `example_data/output` directory. A `labels.json` file contains all annotations in follow format:
```json
{
  "labels": {
    "000000000": "test",
    "000000001": "text2"
  },
  "sizes": {
    "000000000": [
      120,
      32 
    ],
    "000000001": [
      128,
      32 
    ]
  },
  "num-samples": 2
}
```

You can also use `--dataset lmdb` to store image in lmdb file, lmdb file contains follow keys:
- num-samples
- image-000000000
- label-000000000
- size-000000000

You can check config file [example_data/example.py](https://github.com/oh-my-ocr/text_renderer/blob/master/example_data/example.py) to learn how to use text_renderer,
or follow the [Quick Start](https://github.com/oh-my-ocr/text_renderer#quick-start) to learn how to setup configuration
 

## Quick Start
### Prepare file resources
   
- Font files: `.ttf`、`.otf`、`.ttc`
- Background images of any size, either from your business scenario or from publicly available datasets ([COCO](https://cocodataset.org/#home), [VOC](http://host.robots.ox.ac.uk/pascal/VOC/))
- Corpus: text_renderer offers a wide variety of [text sampling methods](https://oh-my-ocr.github.io/text_renderer/corpus/index.html), 
to use these methods, you need to consider the preparation of the corpus from two perspectives：
1. The corpus must be in the target language for which you want to perform OCR recognition
2. The corpus should meets your actual business needs, such as education field, medical field, etc.
- Charset file [Optional but recommend]: OCR models in real-world scenarios (e.g. CRNN) usually support only a limited character set, 
so it's better to filter out characters outside the character set during data generation. 
You can do this by setting the [chars_file](https://oh-my-ocr.github.io/text_renderer/corpus/char_corpus.html) parameter

You can download pre-prepared file resources for this `Quick Start` from here: 

- [simsun.ttf](https://github.com/oh-my-ocr/text_renderer/raw/master/example_data/font/simsun.ttf)
- [background.png](https://github.com/oh-my-ocr/text_renderer/raw/master/example_data/bg/background.png)
- [eng_text.txt](https://github.com/oh-my-ocr/text_renderer/raw/master/example_data/text/eng_text.txt)

Save these resource files in the same directory:
```
workspace
├── bg
│ └── background.png
├── corpus
│ └── eng_text.txt
└── font
    └── simsun.ttf
```

### Create config file
Create a `config.py` file in `workspace` directory. One configuration file must have a `configs` variable

The complete configuration file is as follows:
```python
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
    return_bg_and_mask=False  # 把文字和背景都返回
)

render_rand = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.rand_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg
)

render_enum = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.enum_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg
)

render_eng = dict(
    type='Render',
    height=32,  # 字体的高度限制
    gray=True,
    corpus={{_base_.words_corpus}},  # corpus和corpus_effects要对齐，两者是一一对应的关系
    bg=bg
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
    return_bg_and_mask=False  # 把文字和背景都返回
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
    return_bg_and_mask=False  # 把文字和背景都返回
)

imgaug_emboss = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    corpus_effects=[{{_base_.Padding}}, {{_base_.Emboss}}],
    bg=bg,
    return_bg_and_mask=False  # 把文字和背景都返回
)

curve = dict(
    type='Render',
    corpus=enum_cropus,
    corpus_effects=[{{_base_.Padding}}, {{_base_.Curve}}],
    bg=bg,
    return_bg_and_mask=False  # 把文字和背景都返回
)

vertical_text = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    bg=bg
)

dropouthorizontal = dict(
    type='Render',
    corpus={{_base_.chn_corpus}},
    corpus_effects=[{{_base_.DropoutHorizontal}}],
    bg=bg,
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
    return_bg_and_mask=True  # 把文字和背景都返回
)

generator_cfg = [  # 配置多组不同形式的生成对象，同一组语料尽量配置多个生成组，效果更好
    # render_chn,
    # render_enum,
    # render_eng,
    # render_rand,
    # same_line,
    # extra_text_line,
    # imgaug_emboss,
    # bg_and_text_mask,
    # curve,
    # vertical_text,
    dropouthorizontal
]
```

In the above configuration we have done the following things:

1. Specify the location of the resource file
2. Specified text sampling method: 2 or 3 words are randomly selected from the corpus
3. Configured some effects for generation
   - Perspective transformation [NormPerspectiveTransformCfg](https://oh-my-ocr.github.io/text_renderer/_modules/text_renderer/config.html#NormPerspectiveTransformCfg)
   - Random [Line Effect](https://oh-my-ocr.github.io/text_renderer/effect/line.html)
   - Fix output image height to 32
   - Generate color image. `gray=False`, `SimpleTextColorCfg()`
4. Specifies font-related parameters: `font_size`, `font_dir`

## All Effect/Layout Examples

Find all effect/layout config example at [link](https://github.com/oh-my-ocr/text_renderer/blob/master/example_data/effect_layout_example.py)

- `bg_and_text_mask`: Three images of the same width are merged together horizontally, 
  it can be used to train GAN model like [EraseNet](https://github.com/lcy0604/EraseNet)

|    | Name                                 | Example                                                                                                                                                                      |
|---:|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  0 | bg_and_text_mask                     | ![bg_and_text_mask.jpg](./data/effect_layout_image/bg_and_text_mask.jpg)                                         |
|  1 | char_spacing_compact                 | ![char_spacing_compact.jpg](./data/effect_layout_image/char_spacing_compact.jpg)                                 |
|  2 | char_spacing_large                   | ![char_spacing_large.jpg](./data/effect_layout_image/char_spacing_large.jpg)                                     |
|  3 | color_image                          | ![color_image.jpg](./data/effect_layout_image/color_image.jpg)                                                   |
|  4 | curve                                | ![curve.jpg](./data/effect_layout_image/curve.jpg)                                                               |
|  5 | dropout_horizontal                   | ![dropout_horizontal.jpg](./data/effect_layout_image/dropout_horizontal.jpg)                                     |
|  6 | dropout_rand                         | ![dropout_rand.jpg](./data/effect_layout_image/dropout_rand.jpg)                                                 |
|  7 | dropout_vertical                     | ![dropout_vertical.jpg](./data/effect_layout_image/dropout_vertical.jpg)                                         |
|  8 | emboss                               | ![emboss.jpg](./data/effect_layout_image/emboss.jpg)                                                             |
|  9 | extra_text_line_layout               | ![extra_text_line_layout.jpg](./data/effect_layout_image/extra_text_line_layout.jpg)                             |
| 10 | line_bottom                          | ![line_bottom.jpg](./data/effect_layout_image/line_bottom.jpg)                                                   |
| 11 | line_bottom_left                     | ![line_bottom_left.jpg](./data/effect_layout_image/line_bottom_left.jpg)                                         |
| 12 | line_bottom_right                    | ![line_bottom_right.jpg](./data/effect_layout_image/line_bottom_right.jpg)                                       |
| 13 | line_horizontal_middle               | ![line_horizontal_middle.jpg](./data/effect_layout_image/line_horizontal_middle.jpg)                             |
| 14 | line_left                            | ![line_left.jpg](./data/effect_layout_image/line_left.jpg)                                                       |
| 15 | line_right                           | ![line_right.jpg](./data/effect_layout_image/line_right.jpg)                                                     |
| 16 | line_top                             | ![line_top.jpg](./data/effect_layout_image/line_top.jpg)                                                         |
| 17 | line_top_left                        | ![line_top_left.jpg](./data/effect_layout_image/line_top_left.jpg)                                               |
| 18 | line_top_right                       | ![line_top_right.jpg](./data/effect_layout_image/line_top_right.jpg)                                             |
| 19 | line_vertical_middle                 | ![line_vertical_middle.jpg](./data/effect_layout_image/line_vertical_middle.jpg)                                 |
| 20 | padding                              | ![padding.jpg](./data/effect_layout_image/padding.jpg)                                                           |
| 21 | perspective_transform                | ![perspective_transform.jpg](./data/effect_layout_image/perspective_transform.jpg)                               |
| 22 | same_line_layout_different_font_size | ![same_line_layout_different_font_size.jpg](./data/effect_layout_image/same_line_layout_different_font_size.jpg) |
| 23 | vertical_text                        | ![vertical_text.jpg](./data/effect_layout_image/vertical_text.jpg)                                               |


## Reference
https://oh-my-ocr.github.io/text_renderer
