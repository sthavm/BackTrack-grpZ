from django.forms import ModelForm,forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import *

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
        exclude = ['startDate','endDate','is_active','project','sprintNumber','is_completed','is_current']

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

class CreateDevInviteForm(ModelForm):
    idleDevs=DevTeamMember.objects.filter(project=None)
    class Meta:
        model=InviteMessage
        fields=['receiver']
    def __init__(self,*args,**kwargs):
        super(CreateDevInviteForm,self).__init__(*args,**kwargs)
        self.fields['receiver'].widget = CheckboxSelectMultiple()
        self.fields['receiver'].queryset=User.objects.filter(devteammember__in=self.idleDevs)

class CreateManagerInviteForm(ModelForm):
    class Meta:
        model=InviteMessage
        fields=['receiver']
    def __init__(self,*args,**kwargs):
        manList = kwargs.pop('manList',None)
        super(CreateManagerInviteForm,self).__init__(*args,**kwargs)
        self.fields['receiver'].widget = CheckboxSelectMultiple()
        self.fields['receiver'].queryset=User.objects.filter(manager__in=manList)

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
