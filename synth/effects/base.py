'''
@Time    : 2022/5/30 14:13
@Author  : leeguandon@gmail.com
'''
import random
from abc import abstractmethod
from typing import List, Union, Tuple
from PIL.Image import Image as PILImage
from PIL import PyAccess
from synth.utils import prob, BBox


class Effect:
    def __init__(self, p):
        self.p = p

    def __call__(self, img, text_bbox):
        if prob(self.p):
            return self.apply(img, text_bbox)
        return img, text_bbox

    @abstractmethod
    def apply(self, img: PILImage, text_bbox: BBox):
        """

        Parameters
        ----------
        img : PILImage
            Image to apply effect
        text_bbox : BBox
            bbox of text on input Image

        Returns
        -------
        PILImage:
            Image changed
        BBox:
            Text bbox on image after apply effect.
            Some effects (such as Padding) may modify the relative position of the text in the image.

        """
        pass

    @staticmethod
    def rand_pick(pim, col, row):
        """
        Randomly reset pixel value at [col, row]

        new_pixel_value = random.randint(0, pixel_value)

        Parameters
        ----------
        pim : PyAccess
            Get from pil_img.load()
        col : int
        row : int
        """

        # 在[cowl,row]处随机重置像素值
        pim[col, row] = (
            random.randint(0, pim[col, row][0]),
            random.randint(0, pim[col, row][1]),
            random.randint(0, pim[col, row][2]),
            random.randint(0, pim[col, row][3]),
        )

    @staticmethod
    def fix_pick(pim, col, row, value_range: Tuple[int, int]):
        value = random.randint(*value_range)
        pim[col, row] = (value, value, value, value)
