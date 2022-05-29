'''
@Time    : 2022/5/28 14:10
@Author  : leeguandon@gmail.com
'''
from ..builder import MANAGER

IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".JPG", ".JPEG", ".PNG", ".png", ".bmp", ".BMP"}


@MANAGER.register_module()
class BGManager:
    def __init__(self,
                 bg_dir,
                 pre_load):
        self.bg_paths = []
        self.bg_imgs = []
        self.pre_load = pre_load
