# -*- coding: utf-8 -*-
from django.conf import settings


EXPORTS_SAVE_PATH = getattr(settings, 'MINDMAP_EXPORTS_SAVE_PATH', 'exports/') # relative to MEDIA_ROOT