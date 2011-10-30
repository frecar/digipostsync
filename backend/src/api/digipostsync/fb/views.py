

from models import FacebookToken
from django.http import HttpResponse

from api.digipostsync.user.models import User
import libs.facebook_api.client as fb_client
import json

graph = None

def add_token (request, id):
    
    user = User.objects.get(id=id)
    
    token = FacebookToken.objects.get_or_create(user=user)[0]
    token.token = request.GET['access_token']
    token.save()
    
    return HttpResponse("OK")


def delete_token (request, id):
    FacebookToken.objects.filter(user__id=id).delete()
    
    return HttpResponse("OK")


def get_friends (request, id):
    global graph
    
    user = User.objects.get(id=id)
    graph = fb_client.GraphAPI(user.fb_token.all()[0].token)
    
    user = graph.get_object("me")
    friends = graph.get_connections(user["id"], "friends")
    
    return HttpResponse(json.dumps(friends['data'][:100]))

def get_image (request, id):
    return HttpResponse(graph.get_connections(id, "picture"), mimetype="image/jpeg")
    
    