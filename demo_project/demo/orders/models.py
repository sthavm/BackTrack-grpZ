from django.db import models
from django.forms import ModelForm

# Create your models here.
class Project(models.Model):
    projectID=models.CharField(max_length=4,primary_key=True)
    def __str__(self):
        return self.projectID

class User(models.Model):
    userID=models.CharField(max_length=4,primary_key=True)
    projectID=models.ForeignKey(Project,null=True, blank=True,on_delete=models.CASCADE)
    right=models.CharField(max_length=3)
    def __str__(self):
        return self.userID

class Pbi(models.Model):
    title=models.CharField(max_length=200,primary_key=True)
    projectID=models.ForeignKey(Project, on_delete=models.CASCADE, default='A')
    status=models.CharField(max_length=20, default='NotYetStarted')
    description=models.CharField(max_length=2000)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    storyPt=models.DecimalField(max_digits=2,decimal_places=0)
    def __str__(self):
        return self.title
