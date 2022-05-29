'''
@Time    : 2022/5/28 14:16
@Author  : leeguandon@gmail.com
'''
import os
from typing import Dict

import cv2
import numpy as np


class Dataset:
    def __init__(self, work_dir: str, jpg_quality: int = 95):
        self.work_dir = work_dir
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        self.jpg_quality = jpg_quality

    def encode_param(self):
        return [int(cv2.IMWRITE_JPEG_QUALITY), self.jpg_quality]

    def write(self, name: str, image: np.ndarray, label: str):
        pass

    def read(self, name) -> Dict:
        """

        Parameters
        ----------
            name : str
                000000001

        Returns
        -------
            dict :

                .. code-block:: bash

                    {
                        "image": ndarray,
                        "label": "label",
                        "size": [int_width, int_height]
                    }
        """
        pass

    def read_count(self) -> int:
        pass

    def write_count(self, count: int):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
