# -*- coding: utf-8 -*-
from django.conf import settings
from api.digipostsync.dropbox.models import DropboxToken
from api.digipostsync.dropbox.forms import DropboxTokenForm
from api.digipostsync.user.models import User
from piston.handler import BaseHandler
from piston.utils import rc

class DropboxTokenHandler(BaseHandler):
    model = DropboxToken
    fields = ('id', ('user',('id','username',)), 'token',)

    def read(self, request, id=None):
        all = DropboxToken.objects.all()

        #print get_access_token(User.objects.get(id=1))
        #print build_dropbox_authorize_url(User.objects.get(id=1))

        if id:
            try:
                return all.get(id=id)
            except DropboxToken.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

    def create(self, request):
        instance = User()
        form = DropboxTokenForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form_dropbox_data = form.save(commit=False)

            if DropboxToken.objects.filter(user=form_dropbox_data.user).exists():
                dropbox_token = DropboxToken.objects.get(user=form_dropbox_data.user)
                dropbox_token.password = form_dropbox_data.password
                dropbox_token.save()

            else:
                dropbox_token = form_dropbox_data

            return dropbox_token

        else:
            return form.errors

    def update(self, request, id):
        try:
            user = DropboxToken.objects.get(id=id)
        except DropboxToken.DoesNotExist:
            return rc.NOT_FOUND

        form = DropboxTokenForm(request.PUT, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return user
        else:
            return form.errors

    def delete(self, request, id):
        try:
            user = DropboxToken.objects.get(id=id)
        except DropboxToken.DoesNotExist:
            return rc.NOT_FOUND

        user.delete()

        return rc.DELETED