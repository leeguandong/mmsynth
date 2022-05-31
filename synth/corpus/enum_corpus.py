'''
@Time    : 2022/5/30 19:03
@Author  : leeguandon@gmail.com
'''
from pathlib import Path
from synth.utils import PanicError, random_choice
from .base import Corpus
from ..builder import CORPUS


@CORPUS.register_module()
class EnumCorpus(Corpus):
    def __init__(self,
                 num_pick=1,
                 items=None,
                 *args,
                 **kwargs):
        super(EnumCorpus, self).__init__(*args, **kwargs)
        self.num_pick = num_pick
        self.items = items
        self.join_str: str = ""

        if len(self.text_paths) == 0 and len(self.items) == 0:
            raise PanicError(f"text_paths or items must not be empty")

        if len(self.text_paths) != 0 and len(self.items) != 0:
            raise PanicError(f"only one of text_paths or items can be set")

        self.texts = []

        if len(self.text_paths) != 0:
            for text_path in self.text_paths:
                with open(str(text_path), "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        self.texts.append(line.strip())
        elif len(self.items) != 0:
            self.texts = self.items

        if self.chars_file is not None:
            self.font_manager.update_font_support_chars(self.chars_file)

        if self.filter_by_chars:
            self.texts = Corpus.filter_by_chars(self.texts, self.chars_file)
            if self.filter_font:
                self.font_manager.filter_font_path(
                    self.filter_font_min_support_chars)

    def get_text(self):
        text = random_choice(self.texts, self.num_pick)  # 从列表中随机选择项目
        return self.join_str.join(text)
