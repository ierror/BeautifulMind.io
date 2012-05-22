# -*- coding: utf-8 -*-
from settings import DEBUG


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
