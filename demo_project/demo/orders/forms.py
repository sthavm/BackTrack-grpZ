from django.forms import ModelForm,forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import *

class TeamForm(ModelForm):
    class Meta:
        model=DevTeamMember
        exclude=['user','project']
class ManagerViewForm(ModelForm):
    class Meta:
        model=Manager
        exclude=['user','project']
class ProductOwnerViewForm(ModelForm):
    class Meta:
        model=ProductOwner
        exclude=['user','project']

class PbiCreateForm(ModelForm):
    class Meta:
        model = Pbi
        exclude = ['projectID','status','sprints']
class PbiModifyForm(ModelForm):
    class Meta:
        model = Pbi
        exclude = ['projectID','title','sprints']

class TaskModifyForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['pbi','owner']

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=['projectID']

class CreateSprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ['startDate','endDate','is_active','project','sprintNumber','is_completed','is_current','teamID']

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['owner','status','pbi']

class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        manager= Manager.objects.create(user=user)
        return user

class CreateInviteForm(ModelForm):
    class Meta:
        model=InviteMessage
        fields=['receiver']
    def __init__(self,*args,**kwargs):
        set = kwargs.pop('set', None)
        super(CreateInviteForm,self).__init__(*args,**kwargs)
        self.fields['receiver'].widget = CheckboxSelectMultiple()
        self.fields['receiver'].queryset = set

class DevSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_devteam = True
        user.save()
        dev = DevTeamMember.objects.create(user=user)
        dev.project=None
        return user
