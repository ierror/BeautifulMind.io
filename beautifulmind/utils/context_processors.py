# -*- coding: utf-8 -*-
import sys
from django.conf import settings as django_settings
from beautifulmind import VERSION, get_version


class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: {attr: getattr(django_settings, attr)}

sys.modules[__name__ + '.settings'] = SettingsProcessor()


def version(request):
    return {'VERSION': get_version(VERSION)}