'''
@Time    : 2022/5/28 9:33
@Author  : leeguandon@gmail.com
'''

data_dir = "E:/comprehensive_library/mmsynth/data"
corpus = f"{data_dir}/corpus"
char_dir = f"{data_dir}/char"
font_dir = f"{data_dir}/font"
font_list_dir = f"{data_dir}/font_list"

chn_corpus = dict(
    type='CharCorpus',
    text_paths=[f"{corpus}/chn.txt", f"{corpus}/eng.txt"],
    filter_by_chars=True,  # True，则按字符集过滤文本
    chars_file=f"{char_dir}/chn.txt",  # 字符级，通常对应crnn的keys，不过正常ctc中会有一个unkown来过滤不在keys中的字符
    length=(5, 10),  # 输出文本长度范围，一般输出的图像中的字符在5-10个字左右
    char_spacing=(-0.3, 1.3),  # 绘制带间距的字符，如果是元组，则在[min,max)之间随机选择，设置-1以禁用
    font=dict(
        type='FontManager',
        font_dir=font_dir,
        font_list_file=f"{font_list_dir}/font_list.txt",  # 要从font_dir中加载字体文件名，如果未提供，使用font_dir中所有字体
        font_size=(30, 31),  # 字体大小
    ),

)
