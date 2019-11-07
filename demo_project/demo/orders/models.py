from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import *

# Create your models here.
class Project(models.Model):
    projectID=models.CharField(max_length=4,primary_key=True)
    def __str__(self):
        return self.projectID

class User(AbstractUser):
    is_manager = models.BooleanField('manager status', default=False)
    is_prodowner = models.BooleanField('product owner status', default=False)
    is_devteam = models.BooleanField('development team member status', default=False)

class ProductOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.OneToOneField(Project,on_delete=models.CASCADE)

class DevTeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)


class Pbi(models.Model):
    title=models.CharField(max_length=200,primary_key=True)
    projectID=models.ForeignKey(Project, on_delete=models.CASCADE, default='A')
    status=models.CharField(max_length=20, default='NotYetStarted')
    description=models.CharField(max_length=2000)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    storyPt=models.DecimalField(max_digits=2,decimal_places=0)
    def __str__(self):
        return self.title
