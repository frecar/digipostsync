from django.db import models
from api.digipostsync.user.models import User

class DropboxToken(models.Model):
    user = models.ForeignKey(User, related_name="token")
    token = models.CharField(max_length=200)

    def __unicode__(self):
        return "DropboxToken for user %s: %s" % (self.user, self.token)