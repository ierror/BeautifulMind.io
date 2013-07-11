# -*- coding: utf-8 -*-
from django.conf import settings
import os

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
        'NAME'     :  os.getenv('PGDATABASE'),
        'USER'     :  os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
        'PASSWORD ':  os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
        'HOST'     :  os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST'),
        'PORT'     :  os.getenv('OPENSHIFT_POSTGRESQL_DB_PORT'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'beautifulmind-django-cache-default'
    }
}

MEDIA_URL = 'http://' + os.getenv("OPENSHIFT_APP_DNS") + '/assets/'

if not settings.DEBUG:
    STATIC_URL = '%sstatic/' % (MEDIA_URL)

COMPRESS_ENABLED = True

MINDMAPTORNADO_BIND_PORT = os.getenv("OPENSHIFT_PYTHON_PORT")
MINDMAPTORNADO_BIND_IP = os.getenv("OPENSHIFT_PYTHON_IP")
MINDMAPTORNADO_SERVER = 'http://' + os.getenv("OPENSHIFT_APP_DNS") + '/ws/'

ADMINS = (
    ('Bernhard', 'boerni@beautifulmind.io'),
)
