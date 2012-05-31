# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('mindmap.views',
    url(r'^$', 'index', name='mindmap_index'),
    url(r'^map/new/$', 'map_new', name='mindmap_map_new'),

    url(r'^map/(?P<mindmap_pk>\d+)/components/$', 'map_components', name='mindmap_map_components'),
    url(r'^map/(?P<mindmap_pk>\d+)/component/add/$', 'map_component_add', name='mindmap_map_component_add'),
    url(r'^map/(?P<mindmap_pk>(\d|#)+)/component/(?P<component_pk>(\d|#)+)/update/pos/$', 'map_component_update_pos', name='mindmap_map_component_update_pos'),

    url(r'^map/(?P<mindmap_pk>(\d|#)+)/components/add_offset/$', 'map_components_add_offset', name='mindmap_map_components_add_offset'),

    url(r'^(?P<mindmap_slug>.+)$', 'map_show', name='mindmap_map_show'),
)