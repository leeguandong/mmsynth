'''
@Time    : 2022/5/26 10:27
@Author  : leeguandon@gmail.com
'''
from abc import abstractmethod

from ..utils import retry
from ..builder import build_font


class Corpus:
    def __init__(self,
                 font):
        self.font_manager = build_font(font)

    @retry
    def sample(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @staticmethod
    def filter_by_chars(text, chars_file):
        pass
