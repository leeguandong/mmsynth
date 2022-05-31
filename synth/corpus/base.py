'''
@Time    : 2022/5/26 10:27
@Author  : leeguandon@gmail.com
'''
import os
from abc import abstractmethod
from loguru import logger
from pathlib import Path

from ..utils import retry, PanicError, RetryError, FontText, load_chars_file
from ..builder import build_manager


class Corpus:
    def __init__(self,
                 font,
                 text_paths=[],
                 filter_by_chars=False,
                 chars_file=None,
                 text_color=None,
                 char_spacing=-1,
                 clip_length=-1,
                 horizontal=True,
                 filter_font=False,
                 filter_font_min_support_chars=100,
                 ):
        self.text_paths = text_paths
        self.chars_file = chars_file
        self.filter_by_chars = filter_by_chars
        self.clip_length = clip_length
        self.horizontal = horizontal
        self.char_spacing = char_spacing
        self.filter_font = filter_font
        self.filter_font_min_support_chars = filter_font_min_support_chars
        self.font_manager = build_manager(font)
        self.text_color_manager = build_manager(text_color)

    @retry
    def sample(self):
        try:
            text = self.get_text()  # 获取到多少text，是顺序还是无序，交给子类实现
        except Exception as ee:
            logger.exception(ee)
            raise RetryError()

        # 是否裁剪输出
        if self.clip_length != -1 and len(text) > self.clip_length:
            text = text[: self.clip_length]  # 裁剪get_text的输出，-1禁用

        # font_manager中的核心方法
        font, support_chars, font_path = self.font_manager.get_font()
        status, intersect = self.font_manager.check_support(text, support_chars)
        if not status:
            err_msg = (
                f"{self.__class__.__name__} {font_path} not support chars: {intersect}")
            logger.debug(err_msg)
            raise RetryError(err_msg)

        # FontText 用了dataclass，返回一个数据类
        return FontText(font, text, font_path, self.horizontal)  # 默认是生成水平的 horizontal，设置False

    @abstractmethod
    def get_text(self):
        pass

    @staticmethod
    def filter_by_chars(text, chars_file):
        """
        写成静态方法规范一点，把char字符级中的文字在text中进行保存，
        相当于在选择text合成之前就对text进行过滤
        :param text:
        :param chars_file:
        :return:
        """
        if chars_file is None or not os.path.exists(chars_file):
            raise PanicError(f"chars_file not exists: {chars_file}")

        chars = load_chars_file(chars_file, log=True)

        logger.info("filtering text by chars...")

        total_count = 0
        filtered_count = 0

        # TODO: find a more efficient way
        filtered_chars = []
        if isinstance(text, list):
            out = []
            for t in text:
                _text = ""
                for c in t:
                    if c in chars:
                        _text += c
                    else:
                        filtered_count += 1
                        filtered_chars.append(c)
                    total_count += 1
                out.append(_text)
        else:
            out = ""
            for c in text:
                if c in chars:
                    out += c
                else:
                    filtered_count += 1
                    filtered_chars.append(c)
                total_count += 1
        logger.info(
            f"Filter {(filtered_count/total_count)*100:.2f}%({filtered_count}) chars in input text。"
            f"Unique chars({len(set(filtered_chars))}): {set(filtered_chars)}")
        return out
