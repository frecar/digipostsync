# -*- coding: utf-8 -*-
from api.digipostsync.user.models import User
from piston.handler import BaseHandler
from piston.utils import rc

class UserHandler(BaseHandler):
    model = User
    fields = ('username', 'password',)

    def read(self, request, id=None):
        all = User.objects.all()
        if id:
            try:
                return all.get(id=id)
            except User.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all