from django.forms.models import ModelForm
from api.digipostsync.user.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('id','username','password')