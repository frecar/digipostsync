import urllib2
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
import urllib
from api.digipostsync.dropbox.models import DropboxToken
from api.digipostsync.user.models import User
from libs.dropbox_api import session
import oauth.oauth as oauth

sessions_user = {}

def build_dropbox_authorize_url(user):
    sess = session.DropboxSession(settings.DROPBOX_APP_KEY, settings.DROPBOX_APP_SECRET, 'app_folder')
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)
    sessions_user[user.id] = sess

    return url

def get_access_token(user):
    sess = sessions_user[user.id]
    access_token = sess.obtain_access_token()

    dropbox_token = DropboxToken.objects.get_or_create(user=user)[0]
    dropbox_token.token = access_token.to_string()
    dropbox_token.save()

    return access_token

def get_url_for_auth_dropbox(request, id):
    """
        Visit this url to get the auth url for Dropbox, forward this url to the client
        api/user/{{user_id}}/get_url_for_auth_dropbox/
    """

    url = build_dropbox_authorize_url(User.objects.get(id=id))
    return HttpResponse(simplejson.dumps({'url': url}))

def tell_server_dropbox_token_is_ready_for_user(request, id):
    """
        Visit this url after client has completed the sign in at Dropbox
        api/user/{{user_id}}/tell_server_dropbox_token_is_ready_for_user/
    """

    user = User.objects.get(id=id)

    dropbox_token = DropboxToken.objects.get_or_create(user=user)[0]
    dropbox_token.token = get_access_token(user)

    dropbox_token.save()

    return HttpResponse(dropbox_token.token)

def delete_dropbox_token (request, id):
    DropboxToken.objects.filter(user__id=id).delete()
    
    return HttpResponse("OK")