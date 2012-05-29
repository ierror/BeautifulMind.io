# -*- coding: utf-8 -*-
from .exceptions import HTTPException


def check_for_map_pk_data(method):
    def wrapped(*args, **kwargs):
        # we need map_pk data key
        try:
            args[1]['map_pk'] = int(args[1]['map_pk'])
        except (KeyError, IndexError, ValueError):
            raise HTTPException(log_message='check_for_map_pk_data decorated methods need an integer map_pk data key')

        method(*args, **kwargs)
    return wrapped