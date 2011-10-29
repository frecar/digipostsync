# -*- coding: utf-8 -*-
from api.digipostsync.user.forms import UserForm
from api.digipostsync.user.models import User
from piston.handler import BaseHandler
from piston.utils import rc

class UserHandler(BaseHandler):
    model = User
    fields = ('id', 'username', 'password',)

    def read(self, request, id=None):
        all = User.objects.all()
        if id:
            try:
                return all.get(id=id)
            except User.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

    def create(self, request):
        instance = User()
        form = UserForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form_user_data = form.save(commit=False)

            if User.objects.filter(username=form_user_data.username).exists():
                user = User.objects.get(username=form_user_data.username)
                user.password = form_user_data.password
                user.save()

            else:
                user = form_user_data

            return user

        else:
            return form.errors

    def update(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return rc.NOT_FOUND

        form = UserForm(request.PUT, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return user
        else:
            return form.errors

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return rc.NOT_FOUND

        user.delete()
        
        return rc.DELETED