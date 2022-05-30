'''
@Time    : 2022/5/30 14:12
@Author  : leeguandon@gmail.com
'''
import numpy as np
from typing import Tuple
from PIL.Image import Image as PILImage
from synth.utils import BBox, transparent_img, random_xy_offset
from .base import Effect
from ..builder import EFFECTS


@EFFECTS.register_module()
class Padding(Effect):
    def __init__(self,
                 p=0.5,
                 w_ratio=(0.0, 0.05),
                 h_ratio=(0.0, 0.3),
                 center: bool = False):
        """

        Parameters
        ----------
        p : float
            Probability of apply this effect
        w_ratio : tuple
            [min_ratio, max_ratio)
        h_ratio : tuple
            [min_ratio, max_ratio)
        center : bool
            Center text in image
        """

        super().__init__(p)
        self.w_ratio = w_ratio
        self.h_ratio = h_ratio
        self.center = center

    def apply(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        w_ratio = np.random.uniform(*self.w_ratio)
        h_ratio = np.random.uniform(*self.h_ratio)
        new_w = int(img.width + img.width * w_ratio)
        new_h = int(img.height + img.height * h_ratio)

        new_img = transparent_img((new_w, new_h))

        if self.center:
            xy = (int((new_w - img.width) / 2), int((new_h - img.height) / 2))
        else:
            xy = random_xy_offset(img.size, (new_w, new_h))

        new_img.paste(img, xy)

        new_bbox = text_bbox.move_origin(xy)
        return new_img, new_bbox
