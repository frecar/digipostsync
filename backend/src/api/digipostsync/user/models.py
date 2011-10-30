# -*- coding: utf-8 -*-
import os
import urllib2
from django.conf import settings
from django.db import models
import oauth.oauth as oauth
import urllib
from api.digipostsync.dropbox.models import DropboxUploadedFileHashes
from libs.digipost_api.client import DigipostClient
from libs.dropbox_api import client, rest, session
import md5
import libs.facebook_api.client as fb_client

postboxes = [u"postkasse", u"kjokkenbenk", u"arkiv"]

class User(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    def __unicode__(self):
        return "%s" % self.username

    def get_dropbox_token(self):
        if self.token.all().count():
            return oauth.OAuthToken.from_string(self.token.all()[0].token)
        return False

    def get_dropbox_client(self):
        sess = session.DropboxSession(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, 'app_folder')
        sess.token = self.get_dropbox_token()
        return client.DropboxClient(sess)

    def can_connect_to_dropbox(self):
        try:
            self.get_dropbox_client().account_info()
            return True
        except Exception, e:
            return False
        
    def can_connect_to_facebook(self):
        try:
            fb_client.GraphAPI(self.fb_token.all()[0].token).get_object("me")
            return True
        except Exception, e:
            return False

    def can_connect_to_digipost(self):
        try:
            self.get_digipost_client()
            return True
        except Exception, e:
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

    def get_uploaded_files_hashes(self):
        hashes = []
        for hash in self.dropbox_file_hashes.all():
            hashes.append(hash.hash)
        return hashes

    def get_files_in_folder(self, root_folder):
        client = self.get_dropbox_client()

        files = []

        for file in client.metadata(root_folder)['contents']:
            if not file['is_dir']:
                files.append(file['path'])

        return files

    def create_initial_dropbox_folders(self):
        client = self.get_dropbox_client()

        for box in postboxes:
            if not box in self.get_subfolders("/"):
                client.file_create_folder(box)

    def get_digipost_hashes(self, digipost_client):

        digipost_hashes = {}

        for box in postboxes:

           if not box in digipost_hashes:
               digipost_hashes[box] = []

           for file in digipost_client.get_files(box):
               f = file.get_content().read()
               file_hash = md5.new()
               file_hash.update(f)

               digipost_hashes[box].append(file_hash.hexdigest())

        return digipost_hashes

    def sync_digipost_dropbox(self):
        if not self.can_connect_to_dropbox():
            return

        if not self.can_connect_to_digipost():
            return

        client = self.get_dropbox_client()

        digipost_client = self.get_digipost_client()

        self.create_initial_dropbox_folders()

        #Upload new files in arkiv folder
        self.upload_new_files_into_archive(digipost_client)


        for box in postboxes:
            digipost_hash = self.get_digipost_hashes(digipost_client)

            for file in self.get_files_in_folder(box):
                f = client.get_file(file)
                file_hash = md5.new()
                file_hash.update(f.read())

                #Finner filer som ligger i mapper de ikke ligger i digipost
                if not file_hash.hexdigest() in digipost_hash[box]:

                    for b in postboxes:

                        #Finner hvilken mappe filen egentlig tilhører (om den gjør det)
                        if file_hash.hexdigest() in digipost_hash[b]:
                            
                            for digipost_file in digipost_client.get_files(b):
                                f = digipost_file.get_content().read()
                                file_hash_digipost_file = md5.new()
                                file_hash_digipost_file.update(f)

                                #Fant filens egentlige mappe, dvs, at den ikke er slettet men flyttet.
                                if file_hash.hexdigest() == file_hash_digipost_file.hexdigest():

                                    if box == u"arkiv":
                                        digipost_file.move_to_arkiv()

                                    else:
                                        digipost_file.move_to_kjokkenbenk()
                                        
            digipost_hash = self.get_digipost_hashes(digipost_client)

            dropbox_hashes = []

            for file in self.get_files_in_folder(box):
                f = client.get_file(file)
                file_hash = md5.new()
                file_hash.update(f.read())

                if not file_hash.hexdigest() in digipost_hash[box]:
                    client.file_delete(file.encode("utf-8"))

                dropbox_hashes.append(file_hash.hexdigest())

            for file in digipost_client.get_files(box):
                f = file.get_content().read()
                file_hash = md5.new()
                file_hash.update(f)

                if file_hash.hexdigest() in digipost_hash[box] and file_hash.hexdigest() not in dropbox_hashes:
                    client.put_file('/' + box + "/" + file.emne + ".pdf", f)
                    DropboxUploadedFileHashes.objects.get_or_create(user=self, hash=file_hash.hexdigest())

    def upload_new_files_into_archive(self, digipost_client):
        client = self.get_dropbox_client()

        for file in self.get_files_in_folder("arkiv"):
            f = client.get_file(file)

            file_name = os.path.splitext(file)[0]
            file_name = file_name.split(os.sep)
            file_name = file_name[len(file_name)-1]

            data_from_response = f.read()
            file_hash = md5.new()
            file_hash.update(data_from_response)

            file_to_upload = open("file.pdf", "w+")
            file_to_upload.write(data_from_response)
            file_to_upload.close()

            file_to_upload = open("file.pdf", "rb")

            if not file_hash.hexdigest() in self.get_uploaded_files_hashes():
                digipost_client.upload_file(file_to_upload, file_name)
                
            file_to_upload.close()
            
            os.remove("file.pdf")
