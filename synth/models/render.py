'''
@Time    : 2022/5/26 10:40
@Author  : leeguandon@gmail.com
'''
import cv2
import numpy as np
from PIL import Image
from loguru import logger
from .compose import Compose
from ..utils import retry, PanicError, draw_text_on_bg, BBox, random_xy_offset, transparent_img
from ..builder import RENDER, build_manager, build_corpus, build_layout


@RENDER.register_module()
class Render:
    def __init__(self,
                 corpus,
                 height=32,
                 corpus_effects=[],
                 layout=None,
                 layout_effects=[],
                 gray=True,
                 perspective_transform=None,
                 bg=None,
                 render_effects=[],
                 return_bg_and_mask=False,
                 *args,
                 **kwargs):
        self.height = height
        self.corpus = corpus
        self.corpus_effects = corpus_effects
        self.layout = layout
        self.layout_effects = layout_effects
        self.gray = gray
        self.perspective_transform = perspective_transform
        self.render_effects = render_effects
        self.return_bg_and_mask = return_bg_and_mask

        self.bg_manager = build_manager(bg)
        if perspective_transform is not None:
            self.perspective_transform_manager = build_manager(perspective_transform)

        if isinstance(corpus, list) and isinstance(corpus_effects, list):
            if len(corpus) != len(corpus_effects):
                raise PanicError(
                    f"corpus length({self.corpus}) is not equal to corpus_effects length({self.corpus_effects})")

        # corpus和corpus_effects可能需要对应多组
        if isinstance(self.corpus, list) and len(self.corpus) > 1:
            self.corpus = [build_corpus(corpus) for corpus in self.corpus]
            self.effects = [Compose(corpus_effects) for corpus_effects in self.corpus_effects]
        else:
            self.corpus = build_corpus(self.corpus)
            self.effects = Compose(corpus_effects)

        if self.layout is not None:
            self.layout = build_layout(self.layout)

    @retry
    def forward(self, *args, **kwargs):
        try:
            if isinstance(self.corpus, list) and len(self.corpus) > 1:
                img, text, cropped_bg, transformed_text_mask = self.gen_multi_corpus()
            else:
                img, text, cropped_bg, transformed_text_mask = self.gen_single_corpus()

            if self.render_effects is not None:
                img, _ = Compose(self.render_effects)(img, BBox.from_size(img.size))

            if self.return_bg_and_mask:
                gray_text_mask = np.array(transformed_text_mask.convert("L"))
                _, gray_text_mask = cv2.threshold(
                    gray_text_mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                transformed_text_mask = Image.fromarray(255 - gray_text_mask)

                merge_target = Image.new("RGBA", (img.width * 3, img.height))
                merge_target.paste(img, (0, 0))
                merge_target.paste(cropped_bg, (img.width, 0))
                merge_target.paste(
                    transformed_text_mask,
                    (img.width * 2, 0),
                    mask=transformed_text_mask, )

                np_img = np.array(merge_target)
                np_img = cv2.cvtColor(np_img, cv2.COLOR_RGBA2BGR)
                np_img = self.norm(np_img)
                # cv2.imshow(np_img)
            else:
                img = img.convert("RGB")
                np_img = np.array(img)
                np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
                np_img = self.norm(np_img)
            return np_img, text
        except Exception as ee:
            logger.exception(ee)
            raise ee

    def gen_single_corpus(self):
        # 1.随机获取text，未考虑词频均衡采样
        font_text = self.corpus.sample()

        # 2.获取背景图，bg来源于输入bg图，并非自动生成，也可通过生成加噪声的方式产生背景图
        bg = self.bg_manager.get_bg()

        # 3.文字的颜色生成
        text_color = self.corpus.text_color_manager.get_color(bg)

        # 4.font_text和颜色之后生成的text_mask
        text_mask = draw_text_on_bg(
            font_text, text_color, char_spacing=self.corpus.char_spacing)

        # 5.作用在text_mask上的效果
        if self.corpus_effects is not None:
            text_mask, _ = self.effects(text_mask, BBox.from_size(text_mask.size))

        # 6.添加透视变换
        if self.perspective_transform is not None:
            # TODO: refactor this, now we must call get_transformed_size to call gen_warp_matrix
            _ = self.perspective_transform_manager.get_transformed_size(text_mask.size)

            try:
                (transformed_text_mask, transformed_text_pnts,) = \
                    self.perspective_transform_manager.do_warp_perspective(text_mask)
            except Exception as ee:
                logger.exception(ee)
                logger.error(font_text.font_path, "text", font_text.text)
                raise ee
        else:
            transformed_text_mask = text_mask

        # 7.将text_mask粘贴bg上
        img, cropped_bg = self.paste_text_mask_on_bg(bg, transformed_text_mask)

        return img, font_text.text, cropped_bg, transformed_text_mask

    def gen_multi_corpus(self):
        # 1.corpus 采样
        font_texts = [it.sample() for it in self.corpus]

        # 2.bg图
        bg = self.bg_manager.get_bg()

        text_masks, text_bboxes = [], []
        for i in range(len(font_texts)):
            font_text = font_texts[i]
            _text_color = self.corpus[i].text_color_manager.get_color(bg)
            text_mask = draw_text_on_bg(
                font_text, _text_color, char_spacing=self.corpus[i].char_spacing
            )

            text_bbox = BBox.from_size(text_mask.size)
            if self.corpus_effects is not None:
                effects = self.effects[i]
                if effects is not None:
                    text_mask, text_bbox = effects(text_mask, text_bbox)
            text_masks.append(text_mask)
            text_bboxes.append(text_bbox)

        text_mask_bboxes, merged_text = self.layout(
            font_texts,
            [it.copy() for it in text_bboxes],
            [BBox.from_size(it.size) for it in text_masks],
        )
        if len(text_mask_bboxes) != len(text_bboxes):
            raise PanicError(
                "points and text_bboxes should have same length after layout output")

        merged_bbox = BBox.from_bboxes(text_mask_bboxes)
        merged_text_mask = transparent_img(merged_bbox.size)
        for text_mask, bbox in zip(text_masks, text_mask_bboxes):
            merged_text_mask.paste(text_mask, bbox.left_top)

        if self.perspective_transform is not None:
            # TODO: refactor this, now we must call get_transformed_size to call gen_warp_matrix
            _ = self.perspective_transform_manager.get_transformed_size(merged_text_mask.size)

            (transformed_text_mask, transformed_text_pnts,) = \
                self.perspective_transform_manager.do_warp_perspective(merged_text_mask)
        else:
            transformed_text_mask = merged_text_mask

        if self.layout_effects is not None:
            transformed_text_mask, _ = Compose(self.layout_effects)(
                transformed_text_mask, BBox.from_size(transformed_text_mask.size))

        img, cropped_bg = self.paste_text_mask_on_bg(bg, transformed_text_mask)

        return img, merged_text, cropped_bg, transformed_text_mask

    def paste_text_mask_on_bg(self, bg, transformed_text_mask):
        """

        Args:
            bg:
            transformed_text_mask:

        Returns:

        """
        x_offset, y_offset = random_xy_offset(transformed_text_mask.size, bg.size)
        bg = self.bg_manager.guard_bg_size(bg, transformed_text_mask.size)
        bg = bg.crop(
            (
                x_offset,
                y_offset,
                x_offset + transformed_text_mask.width,
                y_offset + transformed_text_mask.height,
            )
        )
        if self.return_bg_and_mask:  # 把背景和文字都返回
            _bg = bg.copy()
        else:
            _bg = bg
        bg.paste(transformed_text_mask, (0, 0), mask=transformed_text_mask)

        return bg, _bg

    def norm(self, image: np.ndarray) -> np.ndarray:
        if self.gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 调整图像大小（保持比例）到高度，设置-1禁用调整大小
        if self.height != -1 and self.height != image.shape[0]:
            height, width = image.shape[:2]
            width = int(width // (height / self.height))
            image = cv2.resize(
                image, (width, self.height), interpolation=cv2.INTER_CUBIC
            )

        return image
