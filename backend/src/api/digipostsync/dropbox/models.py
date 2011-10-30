# -*- coding: utf-8 -*-
from django.db import models

class DropboxToken(models.Model):
    user = models.ForeignKey('user.User', related_name="token")
    token = models.CharField(max_length=200)

    request_token = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return "DropboxToken for user %s: %s" % (self.user, self.token)


class DropboxUploadedFileHashes(models.Model):
    user = models.ForeignKey('user.User', related_name="dropbox_file_hashes")
    hash = models.CharField(max_length=200)

    folder = models.CharField(max_length=150, default="")
    
    def __unicode__(self):
        return self.hash