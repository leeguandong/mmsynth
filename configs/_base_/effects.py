'''
@Time    : 2022/5/28 15:46
@Author  : leeguandon@gmail.com
'''
Padding = dict(
    type='Padding',
    p=1,
    w_ratio=[0.2, 0.21],
    h_ratio=[0.7, 0.71]
)

Curve = dict(
    type='Curve',
    period=180,
    amplitude=(4, 5)
)

Line = dict(
    type='Line',
    p=0.5,
    color=(255, 50, 0, 255)
)

OneOf = dict(
    type='OneOf',
    effects=[
        dict(type='DropoutRand'),
        dict(type='DropoutVertical')
    ],
)
