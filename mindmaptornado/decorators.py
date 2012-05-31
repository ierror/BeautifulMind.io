# -*- coding: utf-8 -*-
from .exceptions import HTTPException


class check_for_map_pk(object):
    def __call__(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                # we need map_pk data key
                args[1]['map_pk'] = int(args[1]['map_pk'])
            except (KeyError, IndexError, ValueError):
                raise HTTPException(log_message='check_for_map_pk decorated method "%s" needs an integer map_pk data key' % (method.__name__))

            method(*args, **kwargs)
        return wrapped_method


class check_for_component_pk(object):
    def __call__(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                # we need map_pk data key
                args[1]['component_pk'] = int(args[1]['component_pk'])
            except (KeyError, IndexError, ValueError):
                raise HTTPException(log_message='check_for_component_pk decorated method "%s" needs an integer component data key' % (method.__name__))

            method(*args, **kwargs)
        return wrapped_method


class check_for_data(object):
    def __init__(self, *args):
        self.neede_data = args

    def __call__(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                for data in self.neede_data:
                    args[1][data]
            except (KeyError, IndexError):
                raise HTTPException(log_message='check_for_data decorated method "%s" needs "%s" data' % (method.__name__, data))

            method(*args, **kwargs)
        return wrapped_method
