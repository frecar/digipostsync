# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.emitters import Emitter
from piston.resource import Resource
from api.digipostsync.user.handlers import UserHandler

user = Resource(handler=UserHandler)

urlpatterns = patterns('',
                       #Contacts
                       url(r'users/$', user),
                       url(r'users/(?P<id>\d+)/$', user),
)