# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('mindmap.views',
    url(r'^$', 'index', name='mindmap_index'),
    url(r'^map/new/$', 'map_new', name='mindmap_map_new'),
    url(r'^map/(?P<mindmap_pk>\d+)/components/$', 'map_components', name='mindmap_map_components'),
    url(r'^(?P<mindmap_slug>.+)$', 'map_show', name='mindmap_map_show'),
)