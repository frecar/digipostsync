# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.emitters import Emitter
from piston.resource import Resource
from api.digipostsync.dropbox.handlers import DropboxTokenHandler
from api.digipostsync.user.handlers import UserHandler

user = Resource(handler=UserHandler)
dropbox_token = Resource(handler=DropboxTokenHandler)

urlpatterns = patterns('',
                       #Users
                       url(r'users/$', user),
                       url(r'users/(?P<id>\d+)/$', user),

                       #DropboxTokens
                       url(r'dropbox_tokens/$', dropbox_token),
                       url(r'dropbox_tokens/(?P<id>\d+)/$', dropbox_token),
)