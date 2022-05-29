'''
@Time    : 2021/2/19 19:10
@Author  : 19045845
'''
from .compat import Registry


def build(cfg, registry, default_args=None):
    if not isinstance(cfg, dict):
        raise TypeError(f'cfg must be a dict, but got {type(cfg)}')
    if 'type' not in cfg:
        raise KeyError(f'`cfg` must contain the key "type",but got {cfg}')
    if not isinstance(registry, Registry):
        raise TypeError(f'registry must be an tpcv.Registry object,but got {type(registry)}')
    args = cfg.copy()

    if default_args is not None:
        for name, value in default_args.items():
            args.setdefault(name, value)

    obj_type = args.pop("type")
    if isinstance(obj_type, str):
        module = registry.get(obj_type)
        if module is None:
            raise KeyError(f"{obj_type} is not in the {registry.name} registry")
    else:
        raise TypeError(
            f'type must be a str or valid type, but got {type(obj_type)}')

    obj_cls = module(**args)
    return obj_cls
