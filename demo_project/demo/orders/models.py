from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Project(models.Model):
    projectID=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    def __str__(self):
        return self.projectID

class User(AbstractUser):
    is_manager = models.BooleanField('manager status', default=False)
    is_prodowner = models.BooleanField('product owner status', default=False)
    is_devteam = models.BooleanField('development team member status', default=False)
    is_available=models.BooleanField('Available',default=True)
    def __str__(self):
        return self.username

class ProductOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.OneToOneField(Project,on_delete=models.SET_NULL, null=True)

class DevTeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project= models.ManyToManyField(Project)

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    startDate = models.DateField(auto_now_add=True)
    sprintNumber=models.IntegerField(validators=[MinValueValidator(0)])
    durationInDays = models.IntegerField(validators=[MinValueValidator(0)])
    endDate = models.DateField()
    is_active = models.BooleanField('Active Sprint',default=False)
    def setEndDate(self):
        d=datetime.timedelta(days=self.durationInDays)
        self.endDate= datetime.datetime.now() + d

    totalEffortHours = models.IntegerField(validators=[MinValueValidator(0)])
    def active(self):
        if self.endDate > datetime.date.today():
            is_active=True
        else:
            is_active=False


class Pbi(models.Model):
    STATUS_CHOICES=[
        ('Not Started','Not Started'),
        ('In Progress','In Progress'),
        ('Completed','Completed')
    ]
    title=models.CharField(max_length=200)
    projectID=models.ForeignKey(Project, on_delete=models.CASCADE)
    sprints=models.ManyToManyField(Sprint,blank=True)
    status=models.CharField(choices=STATUS_CHOICES, max_length=20, default='Not Started')
    description=models.CharField(max_length=2000)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    storyPt=models.DecimalField(max_digits=2,decimal_places=0)
    class Meta:
        unique_together = (("title", "projectID"),)
    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES=[
        ('Not Started','Not Started'),
        ('In Progress','In Progress'),
        ('Completed','Completed')
    ]

    pbi = models.ForeignKey(Pbi, on_delete=models.CASCADE)
    owner = models.ForeignKey(DevTeamMember,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    effortHours = models.IntegerField(validators=[MinValueValidator(0)])
    hourSpent=models.IntegerField(validators=[MinValueValidator(0)],null=True,blank=True)
    class Meta:
        unique_together = (("title", "pbi"),)

class InviteMessage(models.Model):
    receiver=models.ManyToManyField(User)
    project=models.OneToOneField(Project,on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.project.projectID

# class Sprint_Pbi(models.Model):
#     sprint=models.ForeignKey(Sprint, on_delete=models.CASCADE)
#     project=models.ForeignKey(Project, on_delete=models.CASCADE)
#     pbi=models.ForeignKey(Pbi, on_delete=models.CASCADE)
#     class Meta:
#         unique_together = (("project","sprint", "pbi"),)
