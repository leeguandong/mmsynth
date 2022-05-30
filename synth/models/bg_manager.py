'''
@Time    : 2022/5/28 14:10
@Author  : leeguandon@gmail.com
'''
import numpy as np

from functools import lru_cache
from pathlib import Path
from PIL import Image
from loguru import logger
from synth.utils import random_choice
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
        self.bg_dir = Path(bg_dir)

        for img in self.bg_dir.glob("**/*"):
            if img.suffix in IMAGE_EXTENSIONS:
                if self._is_transparent_image(img):  # bg的alpha通道必须是255的
                    logger.warning(f"Ignore transparent background image, please convert is to JPEG: {img}")
                    continue
                self.bg_paths.append(str(img))
                if pre_load:
                    self.bg_imgs.append(self._get_bg(str(img)))

        assert len(self.bg_imgs) != 0, "background image is empty"

    def _is_transparent_image(self, p: Path):
        pil_img = Image.open(p)
        pil_img = pil_img.convert("RGBA")
        np_img = np.array(pil_img)
        return not np.all(np_img[:, :, 3] == 255)

    def get_bg(self):
        # TODO: add efficient data augmentation
        if self.pre_load:
            return random_choice(self.bg_imgs)

        bg_path = random_choice(self.bg_paths)
        pil_img = self._get_bg(bg_path)

        return pil_img

    def guard_bg_size(self, pil_img, size):
        """
        make sure background size is large than input size
        """
        width, height = size
        # prevent bg image smaller than size
        scale = max(width / pil_img.size[0], height / pil_img.size[1])
        if scale > 1:
            img_width, img_height = pil_img.size
            scaled_width = int(img_width * scale)
            scaled_height = int(img_height * scale)
            pil_img = pil_img.resize((scaled_width, scaled_height))
        return pil_img

    @lru_cache(maxsize=32)
    def _get_bg(self, bg_path: str):
        """
        return RGBA Pillow image
        """
        # 实现一种 cache 机制，可以在一定次数内使用相同的图片
        pil_img = Image.open(bg_path)
        pil_img = pil_img.convert("RGBA")
        return pil_img
