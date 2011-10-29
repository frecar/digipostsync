from django.forms.models import ModelForm
from api.digipostsync.dropbox.models import DropboxToken

class DropboxTokenForm(ModelForm):
    class Meta:
        model = DropboxToken
        fields = ('id','user','token')