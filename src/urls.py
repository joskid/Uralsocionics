# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^subscribe/', include('django_subscribe.urls')),
    (r'^', include('core.urls')),
)
