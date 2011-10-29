# -*- coding: utf-8 -*-
import os
import urllib2
from django.conf import settings
from django.db import models
import oauth.oauth as oauth
import urllib
from libs.dropbox_api import client, rest, session

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

    def get_dropbox_status(self):
        client = self.get_dropbox_client()

        print self.get_subfolders("/")

        return client.account_info()

    def get_subfolders(self, root_folder):
        client = self.get_dropbox_client()

        folders = []

        for folder in client.metadata(root_folder)['contents']:
            if folder['is_dir']:
                folders.append(folder['path'][len(root_folder):])

        return folders
    
    def create_initial_dropbox_folders(self):
        client = self.get_dropbox_client()

        if not u"Postkasse" in self.get_subfolders("/"):
            client.file_create_folder("Postkasse")

        if not u"Kjøkkenbenken" in self.get_subfolders("/"):
            print "hm"
            client.file_create_folder("Kjøkkenbenken")

        if not u"Arkivet" in self.get_subfolders("/"):
            client.file_create_folder("Arkivet")


        self.download_file_and_put_in("http://gfx.dagbladet.no/labrador/188/188175/18817553/jpg/active/978x.jpg","Postkasse", "temp.jpg")

    def download_file_and_put_in(self, url_file, folder, filename):
        urllib.urlretrieve(url_file, filename)
        client = self.get_dropbox_client()

        f = open(filename)
        response = client.put_file('/'+folder+"/"+filename, f)

        os.remove(filename)


    def sync_digipost_dropbox(self):
        client = self.get_dropbox_client()
        #client.file_create_folder("Kjøkkenbenken")

        self.create_initial_dropbox_folders()
        
        return client.metadata("/")