# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from api.digipostsync.user.models import User

class Command(BaseCommand):
    args = ""
    
    def handle(self, *args, **options):
        for user in User.objects.all():
            user.sync_digipost_dropbox()
            print "done for user %s " % user.username