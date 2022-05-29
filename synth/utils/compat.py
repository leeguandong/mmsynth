'''
@Time    : 2022/5/24 17:40
@Author  : leeguandon@gmail.com
'''
try:
    from mmcv.utils import Registry
    from tenacity import retry


except Exception as ee:
    raise ImportError(f'{ee} is not install')
