# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', cache_page(60 * 15)(TemplateView.as_view(template_name='startpage.html'))),

    url(r'^', include('beautifulmind.mindmap.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.ENVIRONMENT.IS_FOR_DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+'../admin_media/', 'show_indexes': True}),
    )