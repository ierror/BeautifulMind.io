# -*- coding: utf-8 -*-
from django.conf.urls import *
from .views_class_based import MapComponentAddView


urlpatterns = patterns('mindmap.views',
    url(r'^map/new/$', 'map_new', name='mindmap_map_new'),

    url(r'^map/(?P<mindmap_pk>(\d|#)+)/component/add/(?P<type>(\w|#|\s)+)/?$', MapComponentAddView.as_view(), name='mindmap_map_component_add'),
    url(r'^map/(?P<mindmap_pk>(\d|#)+)/component/(?P<component_pk>(\d|#)+)/update/pos/$', 'map_component_update_pos', name='mindmap_map_component_update_pos'),
    url(r'^map/(?P<mindmap_pk>(\d|#)+)/component/(?P<component_pk>(\d|#)+)/update/title/$', 'map_component_update_title', name='mindmap_map_component_update_title'),
    url(r'^map/(?P<mindmap_pk>(\d|#)+)/component/(?P<component_pk>(\d|#)+)/delete/$', 'map_component_delete', name='mindmap_map_component_delete'),

    url(r'^map/(?P<mindmap_pk>(\d|#)+)/components/add_offset/$', 'map_components_add_offset', name='mindmap_map_components_add_offset'),
    url(r'^map/(?P<mindmap_pk>(\d|#)+)/components/$', 'map_components', name='mindmap_map_components'),

    url(r'^map/(?P<mindmap_pk>\d+)/export/$', 'map_export', name='mindmap_map_export'),
    url(r'^map/(?P<mindmap_pk>\d+)/export/form/$', 'map_export_form', name='mindmap_map_export_form'),
    url(r'^map/(?P<mindmap_pk>\d+)/export/download/$', 'map_export_download', name='mindmap_map_export_download'),

    url(r'^(?P<mindmap_slug>[0-9]+\-(\w|-)+)$', 'map_show', name='mindmap_map_show'),
)