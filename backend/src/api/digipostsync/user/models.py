from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    def __unicode__(self):
        return "%s" % self.username