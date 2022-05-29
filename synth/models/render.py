'''
@Time    : 2022/5/26 10:40
@Author  : leeguandon@gmail.com
'''
from synth.utils import get_root_logger
from loguru import logger
from ..utils import retry
from ..builder import RENDER


@RENDER.register_module()
class Render:
    def __init__(self,
                 corpus,
                 corpus_effects=None,
                 layout=None,
                 layout_effects=None,
                 gray=True,
                 bg_dir=None,
                 perspective_transform=None
                 ):
        pass

    @retry
    def __call__(self, *args, **kwargs):
        # logger = get_root_logger()
        logger.info("1111111")
        pass

