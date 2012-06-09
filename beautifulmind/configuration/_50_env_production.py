# -*- coding: utf-8 -*-
from django.conf import settings


DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
        'NAME'     : 'beautifulmind',
        'USER'     : 'postgres',
        'PASSWORD ': 'postgres',
        'HOST'     : '127.0.0.1',
        'PORT'     : '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

MEDIA_URL = 'http://beautifulmind.io/assets/'

if not settings.DEBUG:
    STATIC_URL = 'http://beautifulmind.io:8000/assets/static/'

COMPRESS_ENABLED = False

MINDMAPTORNADO_BIND_PORT = 80
MINDMAPTORNADO_SERVER = 'http://beautifulmind.io:%d/ws/' % (MINDMAPTORNADO_BIND_PORT)