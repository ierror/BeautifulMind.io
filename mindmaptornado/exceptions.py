# -*- coding: utf-8 -*-
from tornado.web import HTTPError


class HTTPException(HTTPError):
    def __init__(self, *args, **kwargs):
        super(HTTPException, self).__init__(500, *args, **kwargs)