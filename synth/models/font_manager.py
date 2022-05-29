'''
@Time    : 2022/5/28 11:06
@Author  : leeguandon@gmail.com
'''
from typing import List, Set, Tuple, Dict, Optional
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont
from fontTools.ttLib import TTFont, TTCollection

from ..utils import PanicError, get_root_logger
from ..builder import MANAGER


@MANAGER.register_module()
class FontManager:
    def __init__(self,
                 font_dir,
                 font_list_file,
                 font_size):
        assert font_size[0] < font_size[1]
        self.font_size_min = font_size[0]
        self.font_size_max = font_size[1]
        self.font_paths: List[str] = []
        self.font_support_chars_cache: Dict[str, Set] = {}
        # Created in self.update_font_support_chars(), used to filter font_path
        self.font_support_chars_intersection_with_chars: Dict[str, Set] = {}

        self.logger = get_root_logger()

        if font_list_file is not None:
            with open(str(font_list_file), 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]

            if len(lines) == 0:
                raise PanicError(f'font list file is empty:{font_list_file}')

            for line in lines:
                font_path = font_dir / line
                if font_path.exists():
                    self.font_paths.append(str(font_path))
                else:
                    raise PanicError(f"font file not exist: {font_path}")
        else:
            for font_path in font_dir.glob("**/*"):
                if font_path.suffix in [".ttc", ".TTC", ".ttf", ".TTF", ".otf", ".OTF"]:
                    self.font_paths.append(str(font_path))

        self._load_font_support_chars()

    def _load_font_support_chars(self):
        """
        判断字体是否支持文字的渲染
        :return:
        """
        for font_path in self.font_paths:
            ttf = self._load_ttfont(font_path)

            chars_int = set()
            try:
                for table in ttf["cmap"].tables:
                    for k, v in table.cmap.items():
                        chars_int.add(k)
            except AssertionError as ee:
                self.logger.error(f"Load font file {font_path} failed, skip it. Error: {ee}")

            supported_chars = set([chr(c_int) for c_int in chars_int])
            ttf.close()
            self.font_support_chars_cache[font_path] = supported_chars

    def _load_ttfont(self, font_path: str) -> TTFont:
        """
        Read ttc, ttf, otf font file, return a TTFont object
        """

        # ttc is collection of ttf
        if font_path.endswith("ttc"):
            ttc = TTCollection(font_path)
            # assume all ttfs in ttc file have same supported chars
            return ttc.fonts[0]

        if (font_path.endswith("ttf") or font_path.endswith("TTF")
            or font_path.endswith("otf")):
            ttf = TTFont(font_path, 0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)

            return ttf
