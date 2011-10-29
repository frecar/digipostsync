# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ""
    help = "Run cronjobs in every app.*.cron.py"
    
    def handle(self, *args, **options):
        
        #nclude the Dropbox SDK libraries
        from libs.dropbox_api import client, rest, session
        
        # Get your app key and secret from the Dropbox developer website
        #APP_KEY = 'gyqx9jdvi0c3ms4'
        #APP_SECRET = '7lzaa7cdni90p4k'
        
        # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
        ACCESS_TYPE = 'app_folder'
        
        sess = session.DropboxSession(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, ACCESS_TYPE)
        
        request_token = sess.obtain_request_token()
        
        url = sess.build_authorize_url(request_token)
        
        # Make the user log in and authorize this token
        print "url:", url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()
        
        # This will fail if the user didn't visit the above URL and hit 'Allow'
        access_token = sess.obtain_access_token(request_token)
        
        client = client.DropboxClient(sess)
        print "linked account:", client.account_info()
