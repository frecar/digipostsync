# -*- coding: utf-8 -*-
import os
import urllib2
from django.conf import settings
from django.db import models
import oauth.oauth as oauth
import urllib
from libs.digipost_api.client import DigipostClient
from libs.dropbox_api import client, rest, session
import md5

postboxes = [u"postkasse",u"kjokkenbenk",u"arkiv"]

class User(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    def __unicode__(self):
        return "%s" % self.username

    def get_dropbox_token(self):
        if self.token.all().count():
            return oauth.OAuthToken.from_string(self.token.all()[0].token)

        return ""

    def get_dropbox_client(self):
        sess = session.DropboxSession(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, 'app_folder')
        sess.token = self.get_dropbox_token()
        return client.DropboxClient(sess)

    def can_connect_to_dropbox(self):
        try:
            self.get_dropbox_client()
            return True
        except Exception. e:
            return False

    def can_connect_to_digipost(self):
        try:
            self.get_digipost_client()
            return True
        except Exception. e:
            return False

    def get_digipost_client(self):
        return DigipostClient(self.username, self.password)

    def get_dropbox_status(self):
        client = self.get_dropbox_client()
        return client.account_info()

    def get_subfolders(self, root_folder):
        client = self.get_dropbox_client()

        folders = []

        for folder in client.metadata(root_folder)['contents']:
            if folder['is_dir']:
                folders.append(folder['path'][len(root_folder):])

        return folders

    def get_files_in_folder(self, root_folder):
        client = self.get_dropbox_client()

        folders = []

        for folder in client.metadata(root_folder)['contents']:
            if not folder['is_dir']:
                folders.append(folder['path'])

        return folders

    def create_initial_dropbox_folders(self):
        client = self.get_dropbox_client()

        for box in postboxes:
            if not box in self.get_subfolders("/"):
                client.file_create_folder(box)

    def sync_digipost_dropbox(self):
        if not self.can_connect_to_dropbox():
            return

        if not self.can_connect_to_digipost():
            return

        client = self.get_dropbox_client()
        digipost_client = self.get_digipost_client()
        self.create_initial_dropbox_folders()

        for box in postboxes:
            for file in digipost_client.get_files(box):

                f = file.get_content().read()
                download_file_hash = md5.new()
                download_file_hash.update(f)

                file_exists = False

                for dropbox_file in self.get_files_in_folder(box):

                    current_file_file_hash = md5.new()

                    try:
                        current_file_file_hash.update(client.get_file(dropbox_file).read())
                    except Exception, e:
                        pass

                    if download_file_hash.hexdigest() == current_file_file_hash.hexdigest():
                        file_exists = True
                        continue

                if not file_exists:
                    f = file.get_content().read()
                    client.put_file('/' + box + "/" + file.emne + ".pdf", f)

        return client.metadata("/")
    