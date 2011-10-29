# -*- coding: utf-8 -*-
from django.db import models
from api.digipostsync.user.models import User

class DropboxToken(models.Model):
    user = models.ForeignKey(User, related_name="token")
    token = models.CharField(max_length=200)

    request_token = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return "DropboxToken for user %s: %s" % (self.user, self.token)