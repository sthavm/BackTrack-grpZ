from django.forms import ModelForm
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import *

class PbiCreateForm(ModelForm):
    class Meta:
        model = Pbi
        exclude = ['projectID','status']
class PbiModifyForm(ModelForm):
    class Meta:
        model = Pbi
        exclude = ['projectID','title']

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['projectID']
    def save(self,request):
        user = request.user
        user.is_devteam = False
        user.is_prodowner = True
        prodowner = ProductOwner.objects.create(user=user)
        user.save()



class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user


class DevSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_devteam = True
        user.save()
        dev = DevTeamMember.objects.create(user=user)
        return user
