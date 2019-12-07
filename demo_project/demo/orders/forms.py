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
    hoursLeft = 0
    prevHours = 0
    class Meta:
        model = Task
        exclude = ['pbi','owner','sprint']
    def __init__(self,*args,**kwargs):
        self.hoursLeft = kwargs.pop('sprintHoursLeft', None)
        self.prevHours = kwargs.pop('prevEffortHours', None)
        self.hoursLeft = self.hoursLeft + self.prevHours
        super(TaskModifyForm,self).__init__(*args,**kwargs)
    def clean(self):
        cleaned_data = super(TaskModifyForm, self).clean()
        hoursSpent = cleaned_data.get("hoursSpent")
        effortHours = cleaned_data.get("effortHours")
        if hoursSpent > effortHours:
            raise forms.ValidationError("Effort hours completed must be equal to or less than total effort hours.")
        if effortHours > self.hoursLeft:
            raise forms.ValidationError("The effort hours input exceeds the sprint capacity. Must be less than or equal to "+self.hoursLeft)
class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude=['projectID']

class CreateSprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ['startDate','endDate','is_active','project','sprintNumber','is_completed','is_current','teamID']

class CreateTaskForm(ModelForm):
    hoursLeft = 0
    class Meta:
        model = Task
        exclude = ['owner','status','pbi','sprint','hourSpent']
    def __init__(self,*args,**kwargs):
        self.hoursLeft = kwargs.pop('sprintHoursLeft', None)
        super(CreateTaskForm,self).__init__(*args,**kwargs)
    def clean(self):
        cleaned_data = super(CreateTaskForm, self).clean()
        effortHours = cleaned_data.get("effortHours")
        if effortHours > self.hoursLeft:
            raise forms.ValidationError("This Task has too many effort hours to be included in the current sprint.")

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
