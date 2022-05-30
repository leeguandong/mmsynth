'''
@Time    : 2022/5/30 16:52
@Author  : leeguandon@gmail.com
'''
data_dir = "E:/comprehensive_library/mmsynth/data"
corpus = f"{data_dir}/corpus"
char_dir = f"{data_dir}/chars"
font_dir = f"{data_dir}/fonts"
font_list_dir = f"{data_dir}/fonts_list"

enum_corpus = dict(
    type='EnumCorpus',
    text_paths=[f'{corpus}/enum.txt'],
    filter_by_chars=True,
    chars_file=f'{char_dir}/chn.txt',
    num_pick=1,  # 从文本中随机选择num_pick个项目
    items=[],  # 如果text_paths为空，添加文本
    text_color=dict(
        type='ColorManager',
        alpha=(110, 255)
    ),
    font=dict(
        type='FontManager',
        font_dir=font_dir,
        font_list_file=f"{font_list_dir}/chn.txt",  # 要从font_dir中加载字体文件名，如果未提供，使用font_dir中所有字体
        font_size=(30, 31),  # 字体大小,本意是提供一个范围，这种写法其实就是固定了30
    ),

)
