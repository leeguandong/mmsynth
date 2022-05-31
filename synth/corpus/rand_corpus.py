'''
@Time    : 2022/5/31 10:04
@Author  : leeguandon@gmail.com
'''
import numpy as np
from synth.utils import PanicError, load_chars_file, random_choice
from loguru import logger
from .base import Corpus
from ..builder import CORPUS


@CORPUS.register_module()
class RandCorpus(Corpus):
    def __init__(self,
                 length,
                 text_paths=None,
                 filter_by_chars=False,
                 *args,
                 **kwargs):
        super(RandCorpus, self).__init__(text_paths, filter_by_chars, *args, **kwargs)
        self.length = length

        if self.chars_file is None or not self.chars_file.exists():
            raise PanicError(f"chars_file not exists: {self.chars_file}")

        self.chars = list(load_chars_file(self.chars_file))

        self.font_manager.update_font_support_chars(self.chars_file)
        if self.filter_font:
            self.font_manager.filter_font_path(self.filter_font_min_support_chars)

    def get_text(self):
        length = np.random.randint(*self.length)
        chars = random_choice(self.chars, length)
        text = "".join(chars)
        return text
