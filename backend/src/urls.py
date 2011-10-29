# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (r'^api/', include('api.digipostsync.urls')),


    (r'^api/user/(?P<id>\d+)/delete_dropbox_token/$', 'api.digipostsync.dropbox.views.delete_dropbox_token'),
    (r'^api/user/(?P<id>\d+)/get_url_for_auth_dropbox/', 'api.digipostsync.dropbox.views.get_url_for_auth_dropbox'),
    (r'^api/user/(?P<id>\d+)/tell_server_dropbox_token_is_ready_for_user/', 'api.digipostsync.dropbox.views.tell_server_dropbox_token_is_ready_for_user'),
)