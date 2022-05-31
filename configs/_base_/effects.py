'''
@Time    : 2022/5/28 15:46
@Author  : leeguandon@gmail.com
'''
Padding = dict(
    type='Padding',
    p=1,
    w_ratio=[0.2, 0.21],
    h_ratio=[0.7, 0.71],
    center=True
)

Curve = dict(
    type='Curve',
    period=180,
    amplitude=(4, 5)
)

Line = dict(
    type='Line',
    p=0.5,
    thickness=(1, 3),  # 粗细的范围
    lr_in_offset=(0, 10),  # 左右线内偏移
    lr_out_offset=(0, 5),  # 左右线外偏移
    tb_in_offset=(0, 3),  # 顶底线内偏移
    tb_out_offset=(0, 3),  # 顶底线外偏移
    line_pos_p=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),  # 每个值对应一个位置，总和为1，每种拆成一种，则有10种配置
    color=(255, 50, 0, 255)  # 线的颜色
)

OneOf = dict(
    type='OneOf',
    effects=[
        dict(type='DropoutRand'),
        dict(type='DropoutVertical')
    ],
)

Emboss = dict(
    type='Emboss',
    p=1,
    alpha=(0.9, 1.0),
    strength=(1.5, 1.6)
)

MotionBlur = dict(
    type='MotionBlur',
    p=1.0,
    k=(3, 7),
    angle=(0, 360),
    direction=(-1.0, 1.0)
)

Curve = dict(
    type='Curve',
    p=1.0,
    period=180,  # 三角函数的周期
    amplitude=(4, 5)  # 三角函数的振幅
)

DropoutHorizontal = dict(
    type='DropoutHorizontal',
    p=0.5,
    num_line=3,
    thickness=3
)

DropoutRand = dict(
    type='DropoutRand',
    p=0.5,
    dropout_p=(0.2, 0.4)
)

DropoutVertical = dict(
    type='DropoutVertical',
    p=0.5,
    num_line=8,
    thickness=3
)
