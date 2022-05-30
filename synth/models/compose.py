'''
@Time    : 2022/4/12 13:56
@Author  : leeguandon@gmail.com
'''
import time
import collections
from typing import Tuple
from loguru import logger
from PIL.Image import Image as PILImage
from synth.utils import build_from_cfg, BBox

from ..builder import EFFECTS


class Compose:
    """Compose multiple transforms sequentially.

    Args:
        transforms (Sequence[dict | callable]): Sequence of transform object or
            config dict to be composed.
    """

    def __init__(self, transforms):
        assert isinstance(transforms, collections.abc.Sequence)
        self.transforms = []
        for transform in transforms:
            if isinstance(transform, dict):
                transform = build_from_cfg(transform, EFFECTS)
                self.transforms.append(transform)
            elif callable(transform):
                self.transforms.append(transform)
            else:
                raise TypeError('transform must be callable or a dict')

    def __call__(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        """Call function to apply transforms sequentially.

        Args:
            data (dict): A result dict contains the data to transform.

        Returns:
           dict: Transformed data.
        """
        for t in self.transforms:
            # start = time.time()
            img, text_bbox = t(img, text_bbox)
            # logger.info(f"{t.__class__.__name__} cost {time.time()-start}s")
        return img, text_bbox

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            str_ = t.__repr__()
            if 'Compose(' in str_:
                str_ = str_.replace('\n', '\n    ')
            format_string += '\n'
            format_string += f'    {str_}'
        format_string += '\n)'
        return format_string
