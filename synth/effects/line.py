import typing
import numpy as np
from typing import Tuple
from PIL import ImageDraw
from PIL.Image import Image as PILImage
from synth.utils import transparent_img, BBox

from .base import Effect
from ..builder import EFFECTS


@EFFECTS.register_module()
class Line(Effect):
    def __init__(
            self,
            p=0.5,
            thickness=(1, 3),
            lr_in_offset=(0, 10),  # 左右线内偏移
            lr_out_offset=(0, 5),  # 左右线外偏移
            tb_in_offset=(0, 3),  # 顶底线内偏移
            tb_out_offset=(0, 3),  # 顶底线外偏移
            line_pos_p=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),  # 每个值对应一个位置，总和为1
            color=None,  # 如果不是None，则从cfg获取颜色
    ):
        """
        Draw lines around text

        Args:
            p (float): probability to apply effect
            thickness (int, int): line thickness
            lr_in_offset (int, int): left-right line inner offset
            lr_out_offset (int, int): left-right line outer offset
            tb_in_offset (int, int): top-bottom line inner offset
            tb_out_offset (int, int): top-bottom line outer offset
            line_pos_p (:obj:`tuple`) : Each value corresponds a line position. Must sum to 1.
                        top, bottom, left, right, top_left, top_right, bottom_left, bottom_right, horizontal_middle, vertical_middle
            color_cfg (TextColorCfg): if not None, get color from cfg
        """
        super().__init__(p)
        self.thickness = thickness
        self.lr_in_offset = lr_in_offset
        self.lr_out_offset = lr_out_offset
        self.tb_in_offset = tb_in_offset
        self.tb_out_offset = tb_out_offset
        self.line_pos_p = line_pos_p
        self.color = color

    def apply(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        # TODO: merge apply top/bottom/left.. to make it more efficient
        func = np.random.choice(
            [
                self.apply_top,
                self.apply_bottom,
                self.apply_left,
                self.apply_right,
                self.apply_top_left,
                self.apply_top_right,
                self.apply_bottom_left,
                self.apply_bottom_right,
                self.apply_horizontal_middle,
                self.apply_vertical_middle,
            ],
            p=self.line_pos_p,
        )
        return func(img, text_bbox)

    def apply_horizontal_middle(
            self, img: PILImage, text_bbox: BBox
    ) -> Tuple[PILImage, BBox]:
        row = np.random.randint(1, img.height - 1)
        thickness = np.random.randint(*self.thickness)

        draw = ImageDraw.Draw(img)

        draw.line(
            (0, row, img.width, row),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        return img, text_bbox

    def apply_vertical_middle(
            self, img: PILImage, text_bbox: BBox
    ) -> Tuple[PILImage, BBox]:
        col = np.random.randint(1, img.width - 1)
        thickness = np.random.randint(*self.thickness)

        draw = ImageDraw.Draw(img)

        draw.line(
            (col, 0, col, img.height),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        return img, text_bbox

    def apply_bottom(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        in_offset, thickness, out_offset = self._get_tb_param()
        new_w = img.width
        new_h = img.height + thickness + in_offset + out_offset

        new_img = transparent_img((new_w, new_h))
        new_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(new_img)

        text_bbox.bottom += in_offset
        draw.line(
            list(text_bbox.left_bottom) + list(text_bbox.right_bottom),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        text_bbox.bottom += thickness
        text_bbox.bottom += out_offset

        return new_img, text_bbox

    def apply_top(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        in_offset, thickness, out_offset = self._get_tb_param()

        new_w = img.width
        new_h = img.height + thickness + in_offset

        new_img = transparent_img((new_w, new_h))
        new_img.paste(img, (0, thickness + in_offset + out_offset))

        draw = ImageDraw.Draw(new_img)

        text_bbox.offset_(text_bbox.left_bottom, (0, new_h))
        text_bbox.top -= in_offset
        draw.line(
            list(text_bbox.left_top) + list(text_bbox.right_top),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        text_bbox.top -= thickness
        text_bbox.top -= out_offset

        return new_img, text_bbox

    def apply_right(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        in_offset, thickness, out_offset = self._get_lr_param()

        new_w = img.width + thickness + in_offset + out_offset
        new_h = img.height

        new_img = transparent_img((new_w, new_h))
        new_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(new_img)

        text_bbox.right += in_offset
        draw.line(
            list(text_bbox.right_top) + list(text_bbox.right_bottom),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        text_bbox.right += thickness
        text_bbox.right += out_offset

        return new_img, text_bbox

    def apply_left(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        in_offset, thickness, out_offset = self._get_lr_param()

        new_w = img.width + thickness + in_offset + out_offset
        new_h = img.height

        new_img = transparent_img((new_w, new_h))
        new_img.paste(img, (thickness + in_offset + out_offset, 0))

        draw = ImageDraw.Draw(new_img)

        text_bbox.offset_(text_bbox.right_top, (new_w, 0))
        text_bbox.left -= in_offset

        draw.line(
            list(text_bbox.left_top) + list(text_bbox.left_bottom),
            fill=self._get_line_color(img, text_bbox),
            width=thickness,
        )

        text_bbox.left -= thickness
        text_bbox.left -= out_offset

        return new_img, text_bbox

    def apply_top_left(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        ret = self.apply_top(img, text_bbox)
        return self.apply_left(*ret)

    def apply_top_right(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        ret = self.apply_top(img, text_bbox)
        return self.apply_right(*ret)

    def apply_bottom_left(
            self, img: PILImage, text_bbox: BBox
    ) -> Tuple[PILImage, BBox]:
        ret = self.apply_bottom(img, text_bbox)
        return self.apply_left(*ret)

    def apply_bottom_right(
            self, img: PILImage, text_bbox: BBox
    ) -> Tuple[PILImage, BBox]:
        ret = self.apply_bottom(img, text_bbox)
        return self.apply_right(*ret)

    def _get_lr_param(self) -> Tuple[int, int, int]:
        in_offset = np.random.randint(*self.lr_in_offset)
        out_offset = np.random.randint(*self.lr_out_offset)
        thickness = np.random.randint(*self.thickness)
        return in_offset, thickness, out_offset

    def _get_tb_param(self) -> Tuple[int, int, int]:
        in_offset = np.random.randint(*self.tb_in_offset)
        out_offset = np.random.randint(*self.tb_out_offset)
        thickness = np.random.randint(*self.thickness)
        return in_offset, thickness, out_offset

    def _get_line_color(self, img: PILImage, text_bbox: BBox):
        if self.color is not None:
            # TODO: pass background image
            return self.color

        return (
            np.random.randint(0, 170),
            np.random.randint(0, 170),
            np.random.randint(0, 170),
            np.random.randint(90, 255),
        )
