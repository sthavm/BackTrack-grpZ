from django.forms import ModelForm
from .models import Pbi

class PbiForm(ModelForm):
    class Meta:
        model = Pbi
        exclude = ['projectID']
