# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.contrib import admin

admin.autodiscover()
    
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^subscribe/', include('subscribe.urls')),
    (r'^', include('src.core.urls')),
)

