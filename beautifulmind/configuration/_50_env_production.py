# -*- coding: utf-8 -*-
from django.conf import settings


DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
        'NAME'     : 'beautifulmind',
        'USER'     : 'postgres',
        'PASSWORD ': 'postgres',
        'HOST'     : '127.0.0.1',
        'PORT'     : '6432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'beautifulmind-django-cache-default'
    }
}

MEDIA_URL = 'http://beautifulmind.io/assets/'

if not settings.DEBUG:
    STATIC_URL = 'http://beautifulmind.io/assets/static/'

COMPRESS_ENABLED = True
DEBUG = True

MINDMAPTORNADO_BIND_PORT = 8001
MINDMAPTORNADO_SERVER = 'http://beautifulmind.io/ws/'
