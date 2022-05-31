'''
@Time    : 2022/5/31 16:16
@Author  : leeguandon@gmail.com
'''
import imgaug.augmenters as iaa
import numpy as np
from PIL import Image
from .base import Effect
from ..builder import EFFECTS


@EFFECTS.register_module()
class Emboss(Effect):
    def __init__(self,
                 p=1,
                 alpha=(0.9, 1.0),
                 strength=(1.5, 1.6)):
        super(Emboss, self).__init__(p)
        self.aug = iaa.Emboss(alpha, strength)

    def apply(self, img, text_bbox):
        if self.aug is None:
            return img, text_bbox

        word_img = np.array(img)
        # TODO: test self.aug.augment_bounding_boxes()
        return Image.fromarray(self.aug.augment_image(word_img)), text_bbox


@EFFECTS.register_module()
class MotionBlur(Effect):
    def __init__(self,
                 p=1.0,
                 k=(3, 7),
                 angle=(0, 360),
                 direction=(-1.0, 1.0)):
        super(MotionBlur, self).__init__(p)
        self.aug = iaa.MotionBlur(k, angle, direction)

    def apply(self, img, text_bbox):
        if self.aug is None:
            return img, text_bbox

        word_img = np.array(img)
        # TODO: test self.aug.augment_bounding_boxes()
        return Image.fromarray(self.aug.augment_image(word_img)), text_bbox
