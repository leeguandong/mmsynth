'''
@Time    : 2022/5/29 17:42
@Author  : leeguandon@gmail.com
'''
import cv2
import random
import numpy as np
from typing import Tuple
from loguru import logger
from synth.utils import PanicError

SPACE_CHAR = " "


def prob(percent):
    """
    percent: 0 ~ 1, e.g: 如果 percent=0.1，有 10% 的可能性
    """
    assert 0 <= percent <= 1
    if random.uniform(0, 1) <= percent:
        return True
    return False


def random_choice(items, size=1):
    # np.random.choice is very slow,use np.random.randint
    out = []
    for _ in range(size):
        i = np.random.randint(0, len(items))
        out.append(items[i])
    if size == 1:
        return out[0]
    return out


def random_xy_offset(small_size, big_size) -> Tuple[int, int]:
    """
    Get random left-top point for putting a small rect in a large rect.
    Args:
        small_size: (width, height)
        big_size: (width, height)

    Returns:

    """
    small_rect_width, small_rect_height = small_size
    big_rect_width, big_rect_height = big_size

    y_max_offset = 0
    if big_rect_height > small_rect_height:
        y_max_offset = big_rect_height - small_rect_height

    x_max_offset = 0
    if big_rect_width > small_rect_width:
        x_max_offset = big_rect_width - small_rect_width

    y_offset = 0
    if y_max_offset != 0:
        y_offset = random.randint(0, y_max_offset)

    x_offset = 0
    if x_max_offset != 0:
        x_offset = random.randint(0, x_max_offset)

    return x_offset, y_offset


def size_to_pnts(size) -> np.ndarray:
    """
    获得图片 size 的四个角点 (4,2)
    """
    width = size[0]
    height = size[1]
    return np.array([[0, 0], [width, 0], [width, height], [0, height]])


def load_chars_file(chars_file, log=False):
    """

    Args:
        chars_file (Path): one char per line
        log (bool): Whether to print log

    Returns:
        Set: chars in file

    """
    assumed_space = False
    with open(str(chars_file), "r", encoding="utf-8") as f:
        lines = f.readlines()
        _lines = []
        for i, line in enumerate(lines):
            line_striped = line.strip()
            if len(line_striped) > 1:
                raise PanicError(
                    f"Line {i} in {chars_file} is invalid, make sure one char one line"
                )

            if len(line_striped) == 0 and SPACE_CHAR in line:
                if assumed_space is True:
                    raise PanicError(f"Find two space in {chars_file}")

                if log:
                    logger.info(f"Find space in line {i} when load {chars_file}")
                assumed_space = True
                _lines.append(SPACE_CHAR)
                continue

            _lines.append(line_striped)

        lines = _lines
        chars = set("".join(lines))
    if log:
        logger.info(f"load {len(chars)} chars from: {chars_file}")
    return chars
