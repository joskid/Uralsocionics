# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from src.core.views import *

urlpatterns = patterns('',
    url(r'^category/(\d+)', category, name='category'),
    url(r'^article/(\d+)', article, name='article'),
    url(r'^edition/(\d+)', edition, name='edition'),
    url(r'^tag/(\d+)', tag, name='tag'),
    url(r'^schedule', schedule, name='schedule'),
    url(r'^sitemap', sitemap, name='sitemap'),
    url(r'^order', order, name='order'),
    url(r'^ask', ask, name='ask'),

    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^registration/', registration, name='registration'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^$', index, name='index'),
    )
