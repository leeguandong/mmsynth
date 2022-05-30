'''
@Time    : 2022/5/26 10:25
@Author  : leeguandon@gmail.com
'''
import os
import numpy as np
from loguru import logger
from synth.utils import PanicError
from .base import Corpus
from ..builder import CORPUS


@CORPUS.register_module()
class CharCorpus(Corpus):
    def __init__(self,
                 length,
                 *args,
                 **kwargs):
        super(CharCorpus, self).__init__(*args, **kwargs)
        self.length = length

        self.text = ""

        if len(self.text_paths) == 0:
            raise PanicError(f"text_paths must not contain path")

        for p in self.text_paths:
            if not os.path.exists(p):
                raise PanicError(f"text_path not exists: {p}")

            logger.info(f"load: {p}")
            with open(p, "r", encoding="utf-8") as f:
                self.text += "".join(f.readlines())

        # 字体支持筛选,char_file是字符集的keys
        if self.chars_file is not None:
            self.font_manager.update_font_support_chars(self.chars_file)

        # 按照keys过滤字体中的文字
        if self.filter_by_chars:
            self.text = Corpus.filter_by_chars(self.text, self.chars_file)  # 过滤后的语料
            if self.filter_font:
                self.font_manager.filter_font_path(self.filter_font_min_support_chars)

        if len(self.text) < self.length[1]:
            raise PanicError("too few texts")  # 抛完一场，直接retry

    def get_text(self):
        """
        在语料中随机选择
        :return:
        """
        length = np.random.randint(*self.length)
        start = np.random.randint(0, len(self.text) - length)
        word = self.text[start: start + length]
        return word
