

from urllib2 import urlopen, HTTPError, Request, HTTPCookieProcessor

import json
import urllib2

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
        self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        
        try:
            resp = self._opener.open(self.URL_LOGIN, 'foedselsnummer=%s&passord=%s' % (username, password))
        except HTTPError as e:
            if e.code == 403:
                raise DigipostError('Wrong username/password')
            else:
                raise e
            
        self.konto = self._read(self.URL_KONTO)
        
    def _read (self, url, data=None, format="JSON"):
        """
        Send a GET (or POST, if data is present) request, with 
        the login-cookie attached
        """
        
        resp = self._opener.open(url, data)
        
        if format == "JSON":
            return json.load(resp)
        else:
            return resp.read()
        
    def get_files (self, inbox):
        
        if not inbox + 'Uri' in self.konto:
            raise DigipostError('Did not find an URI for "%s" in this account; Typo?' % inbox)
        
        url = self.konto[inbox + 'Uri']
        return [DigipostFile(data, self) for data in self._read(url)]
    
class DigipostFile (object):
    
    def __init__ (self, data, client):
        self.__dict__ = data
        self._client = client

    def __repr__ (self):
        return self.emne
    
    def get_content (self):
        return self._client._opener.open(self.brevUri)
    
    def move_to_kjokkenbenk (self):
        self._client._read(self.tilKjokkenbenkUri, {'token':self._client.konto['token']}, None)

    def move_to_arkiv (self):
        self._client._read(self.arkiverUri, {'token':self._client.konto['token']}, None)