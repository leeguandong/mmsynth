'''
@Time    : 2022/5/31 9:26
@Author  : leeguandon@gmail.com
'''

data_dir = "E:/comprehensive_library/mmsynth/data"
corpus = f"{data_dir}/corpus"
char_dir = f"{data_dir}/chars"
font_dir = f"{data_dir}/fonts"
font_list_dir = f"{data_dir}/fonts_list"

words_corpus = dict(
    type='WordCorpus',
    text_paths=[ f"{corpus}/eng.txt"],
    filter_by_chars=True,  # True，则按字符集过滤文本
    chars_file=f"{char_dir}/eng.txt",  # 字符级，通常对应crnn的keys，不过正常ctc中会有一个unkown来过滤不在keys中的字符
    num_word=(1, 5),

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
