'''
@Time    : 2022/5/28 9:33
@Author  : leeguandon@gmail.com
'''

data_dir = "E:/comprehensive_library/mmsynth/data"
corpus = f"{data_dir}/corpus"
char_dir = f"{data_dir}/chars"
font_dir = f"{data_dir}/fonts"
font_list_dir = f"{data_dir}/fonts_list"

chn_corpus = dict(
    type='CharCorpus',
    text_paths=[f"{corpus}/chn.txt", f"{corpus}/eng.txt"],
    filter_by_chars=True,  # True，则按字符集过滤文本
    chars_file=f"{char_dir}/chn.txt",  # 字符级，通常对应crnn的keys，不过正常ctc中会有一个unkown来过滤不在keys中的字符
    length=(5, 10),  # 输出文本长度范围，一般输出的图像中的字符在5-10个字左右
    char_spacing=(-0.3, 1.3),  # 绘制带间距的字符，如果是元组，则在[min,max)之间随机选择，设置-1以禁用
    filter_font=False,  # 仅在filter_by_chars为True时有效。如果为True,则通过字体支持的字符与字符文件的字符取交集为过滤字体文件
    filter_font_min_support_chars=100,  # 如果字体支持字符和字符文件的交集低于filter_font_min_support_chars，则过滤此字体文件
    clip_length=-1,  # 裁剪get_text的输出，-1禁用
    horizontal=True,  # 默认是生成水平的 horizontal，设置False

    text_color=dict(
        type='ColorManager',
        alpha=(110, 255)
    ),
    font=dict(
        type='FontManager',
        font_dir=font_dir,
        font_list_file=f"{font_list_dir}/chn.txt",  # 要从font_dir中加载字体文件名，如果未提供，使用font_dir中所有字体
        font_size=(30, 35),  # 字体大小,本意是提供一个范围，这种写法其实就是固定了30
    ),

)
