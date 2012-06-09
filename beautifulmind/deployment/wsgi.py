# -*- coding: utf-8 -*-
import os, sys


# put the Django project on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')

os.environ['DJANGO_SETTINGS_MODULE'] = 'beautifulmind.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()