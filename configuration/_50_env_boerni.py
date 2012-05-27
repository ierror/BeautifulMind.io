# -*- coding: utf-8 -*-
import settings


DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
        'NAME'     : 'beautifulmind',
        'USER'     : 'boerni',
        'PASSWORD ': '',
        'HOST'     : '127.0.0.1',
        'PORT'     : '',
    }
}

MEDIA_URL = 'http://localhost:8000/assets/'

if not settings.DEBUG:
    STATIC_URL = 'http://localhost:8000/assets/static/'

COMPRESS_ENABLED = False

MINDMAPTORNADO_SERVER = 'http://192.168.100.200:1234/echo'