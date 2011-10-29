# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^api/', include('api.digipostsync.urls')),
)