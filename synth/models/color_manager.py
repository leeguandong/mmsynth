'''
@Time    : 2022/5/30 10:42
@Author  : leeguandon@gmail.com
'''
import numpy as np
from ..builder import MANAGER


@MANAGER.register_module()
class ColorManager:
    def __init__(self, alpha):
        self.alpha = alpha

    def get_color(self, bg_img):
        np_img = np.array(bg_img)
        mean = np.mean(np_img)

        alpha = np.random.randint(*self.alpha)
        r = np.random.randint(0, int(mean * 0.7))
        g = np.random.randint(0, int(mean * 0.7))
        b = np.random.randint(0, int(mean * 0.7))
        text_color = (r, g, b, alpha)

        return text_color


@MANAGER.register_module()
class ColorFixManager:
    def __init__(self, color):
        self.color = color

    def get_color(self, bg_img=None):
        return self.color
