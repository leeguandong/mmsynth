'''
@Time    : 2022/5/30 19:58
@Author  : leeguandon@gmail.com
'''
import numpy as np
from typing import List
from loguru import logger
from synth.utils import PanicError
from .base import Corpus
from ..builder import CORPUS


@CORPUS.register_module()
class WordCorpus(Corpus):
    def __init__(self,
                 separator: str = " ",
                 num_word=(1, 5),
                 *args,
                 **kwargs):
        super(WordCorpus, self).__init__(*args, **kwargs)
        self.separator = separator
        self.num_word = num_word

        if len(self.text_paths) == 0:
            raise PanicError("text_paths must not be empty")

        self.words: List[str] = []

        texts = []
        for text_path in self.text_paths:
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()
                texts.append(text.strip())

        if self.chars_file is not None:
            self.font_manager.update_font_support_chars(self.chars_file)

        if self.filter_by_chars:
            texts = Corpus.filter_by_chars(texts, self.chars_file)
            if self.filter_font:
                self.font_manager.filter_font_path(self.filter_font_min_support_chars)

        for text in texts:
            self.words.extend(text.split(self.separator))

        logger.info(f"Load {len(self.words)} words")

        if len(self.words) < self.num_word[1]:
            raise PanicError("too few words")

    def get_text(self):
        if self.num_word[0] == self.num_word[1]:
            length = self.num_word[0]
        else:
            length = np.random.randint(*self.num_word)

        start = np.random.randint(0, len(self.words) - length + 1)
        words = self.words[start: start + length]
        word = self.separator.join(words)
        return word
