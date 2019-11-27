from django.forms import ModelForm,forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
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
        exclude = ['pbi','creator']

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=[]

class CreateSprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ['endDate','is_active','project']

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['creator','status','pbi']

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
        dev.project=None
        return user
