# -*- coding: utf-8 -*-
from .exceptions import HTTPException


class check_for_data(object):
    def __init__(self, *args, **kwargs):
        self.neede_data = args
        self.options = kwargs

    def __call__(self, method):
        def wrapped_method(*args, **kwargs):
            try:
                for data in self.neede_data:
                    data_value = args[1][data]

                    if self.options.get('force_int', False):
                        try:
                            args[1][data] = int(data_value)
                        except (ValueError, TypeError):
                            raise HTTPException(log_message='field "%s" for check_for_data decorated method "%s" with option "force_int" needs to be an integer' % (data, method.__name__))

            except (KeyError, IndexError):
                raise HTTPException(log_message='check_for_data decorated method "%s" needs "%s" data' % (method.__name__, data))

            method(*args, **kwargs)
        return wrapped_method
