'''
@Time    : 2022/5/28 14:19
@Author  : leeguandon@gmail.com
'''
import os
import json
import cv2
import numpy as np

from typing import Dict
from .base import Dataset
from ..builder import DATASET


@DATASET.register_module()
class ImgDataset(Dataset):
    """
    Save generated image as jpg file, save label and meta in json
    json file format:

    .. code-block:: bash

        {
             "labels": {
                "000000000": "test",
                "000000001": "text2"
             },
             "sizes": {
                "000000000": [width, height],
                "000000001": [width, height],
             }
             "num-samples": 2,
        }
    """

    LABEL_NAME = "labels.json"

    def __init__(self, work_dir: str):
        super().__init__(work_dir)
        self._img_dir = os.path.join(work_dir, "images")
        if not os.path.exists(self._img_dir):
            os.makedirs(self._img_dir)
        self._label_path = os.path.join(work_dir, self.LABEL_NAME)

        self._data = {"num-samples": 0, "labels": {}, "sizes": {}}
        if os.path.exists(self._label_path):
            with open(self._label_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)

    def write(self, name: str, image: np.ndarray, label: str):
        img_path = os.path.join(self._img_dir, name + ".jpg")
        cv2.imwrite(img_path, image, self.encode_param())
        self._data["labels"][name] = label

        height, width = image.shape[:2]
        self._data["sizes"][name] = (width, height)

    def read(self, name: str) -> Dict:
        img_path = os.path.join(self._img_dir, name + ".jpg")
        image = cv2.imread(img_path)
        label = self._data["labels"][name]
        size = self._data["sizes"][name]
        return {"image": image, "label": label, "size": size}

    def read_size(self, name: str) -> [int, int]:
        return self._data["sizes"][name]

    def read_count(self) -> int:
        return self._data.get("num-samples", 0)

    def write_count(self, count: int):
        self._data["num-samples"] = count

    def close(self):
        with open(self._label_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
