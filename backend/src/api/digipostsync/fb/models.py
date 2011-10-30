
from django.db import models

class FacebookToken(models.Model):
    user = models.ForeignKey('user.User', related_name="fb_token")
    token = models.CharField(max_length=200)

    request_token = models.CharField(max_length=500, default="")

    def __unicode__(self):
        return "DropboxToken for user %s: %s" % (self.user, self.token)