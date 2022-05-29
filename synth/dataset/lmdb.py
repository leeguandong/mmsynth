'''
@Time    : 2022/5/28 14:20
@Author  : leeguandon@gmail.com
'''
from typing import Dict

import lmdb
import cv2
import numpy as np
from .base import Dataset
from ..builder import DATASET


@DATASET.register_module()
class LmdbDataset(Dataset):
    """
    Save generated image into lmdb. Compatible with https://github.com/PaddlePaddle/PaddleOCR
    Keys in lmdb:

        - image-000000001: image raw bytes
        - label-000000001: string
        - size-000000001: "width,height"

    """

    def __init__(self, work_dir: str):
        super().__init__(work_dir)
        self._lmdb_env = lmdb.open(self.work_dir, map_size=1099511627776)  # 1T
        self._lmdb_txn = self._lmdb_env.begin(write=True)

    def write(self, name: str, image: np.ndarray, label: str):
        self._lmdb_txn.put(
            self.image_key(name),
            cv2.imencode(".jpg", image, self.encode_param())[1].tobytes(),
        )
        self._lmdb_txn.put(self.label_key(name), label.encode())

        height, width = image.shape[:2]
        self._lmdb_txn.put(self.size_key(name), f"{width},{height}".encode())

    def read(self, name: str) -> Dict:
        label = self._lmdb_txn.get(self.label_key(name)).decode()
        size_str = self._lmdb_txn.get(self.size_key(name)).decode()
        size = [int(it) for it in size_str.split(",")]

        image_bytes = self._lmdb_txn.get(self.image_key(name))
        image_buf = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_buf, cv2.IMREAD_UNCHANGED)

        return {"image": image, "label": label, "size": size}

    def read_size(self, name: str) -> [int, int]:
        """

        Args:
            name:

        Returns: (width, height)

        """
        size_key = f"size_{name}"

        size = self._lmdb_txn.get(size_key.encode()).decode()
        width = int(size.split[","][0])
        height = int(size.split[","][1])

        return width, height

    def read_count(self) -> int:
        count = self._lmdb_txn.get("num-samples".encode())
        if count is None:
            return 0
        return int(count)

    def write_count(self, count: int):
        self._lmdb_txn.put("num-samples".encode(), str(count).encode())

    def image_key(self, name: str):
        return f"image-{name}".encode()

    def label_key(self, name: str):
        return f"label-{name}".encode()

    def size_key(self, name: str):
        return f"size-{name}".encode()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lmdb_txn.__exit__(exc_type, exc_value, traceback)
        self._lmdb_env.close()
