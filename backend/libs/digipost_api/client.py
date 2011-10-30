# -*- coding: utf-8 -*-

from urllib2 import urlopen, HTTPError, Request, HTTPCookieProcessor
from urllib import urlencode

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import urllib2
import json
import cookielib

class DigipostError (Exception):
    pass

class DigipostClient(object):
    
    URL = "https://www.digipost.no/"
    URL_LOGIN = URL + 'post/passordautentisering'
    URL_KONTO = URL + 'post/privat/konto'
    
    def __init__ (self, username, password):
        self._login(username, password)
        
    def _login (self, username, password):
        
        # Let's remember those cookies, so use this thing to open urls
        self._opener = register_openers()
        self._opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        
        try:
            resp = self._opener.open(self.URL_LOGIN, 'foedselsnummer=%s&passord=%s' % (username, password))
        except HTTPError as e:
            if e.code == 403:
                raise DigipostError('Wrong username/password')
            else:
                raise e
            
        self.konto = self._json(self.URL_KONTO)
        
    def _read (self, url, data=None, format=None, headers={}, encode=True):
        """
        Send a GET (or POST, if data is present) request, with 
        the login-cookie attached
        """
        
        if isinstance(data, dict) and encode:
            data = urlencode(data)
        
        request = urllib2.Request(url, data, headers)
        result = urllib2.urlopen(request)
        
        if format == "JSON" and result != "":
            return json.load(result)
        else:
            return result.read()
        
    def _json (self, *args, **kwargs):
        kwargs.update({'format': 'JSON'})
        return self._read(*args, **kwargs)
        
    def get_files (self, inbox):
        
        if not inbox + 'Uri' in self.konto:
            raise DigipostError('Did not find an URI for "%s" in this account; Typo?' % inbox)
        
        url = self.konto[inbox + 'Uri']
        return [DigipostFile(data, self) for data in self._json(url)]

    def upload_file (self, file, name):

        datagen, headers = multipart_encode({'fil': file, 'emne': name, 'token': self.konto['token']})
        
        try: 
            return self._read(self.konto['dokumentopplastingUri'], datagen, headers=headers, format=None)
        except HTTPError as e:
            print e.read()
    
    
class DigipostFile (object):
    
    def __init__ (self, data, client):
        self.__dict__ = data
        self._client = client

        
    def __repr__ (self):
        return self.emne
    
    def get_content (self):
        return self._client._opener.open(self.brevUri)
    
    def move_to_kjokkenbenk (self):
        return self._client._read(self.tilKjokkenbenkUri, {'token': self._client.konto['token']})
        
    def move_to_arkiv (self):
        return self._client._read(self.arkiverUri, {'token': self._client.konto['token']})