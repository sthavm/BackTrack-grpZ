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
    sprintView =models.CharField(max_length=2, default='A')

class DevTeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    teamID =models.CharField(max_length=2, default='A')

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project= models.ManyToManyField(Project)
    sprintView =models.CharField(max_length=2, default='A')

class Sprint(models.Model):
    teamID=models.CharField(max_length=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sprintNumber=models.IntegerField(validators=[MinValueValidator(0)])
    startDate = models.DateField(null=True, blank=True)
    durationInDays = models.IntegerField(validators=[MinValueValidator(0)])
    endDate = models.DateField(null=True, blank=True)
    is_active = models.BooleanField('Active Sprint',default=False)
    is_current = models.BooleanField('Current Sprint',default=True)
    is_completed = models.BooleanField('Completed Sprint',default=False)
    totalEffortHours = models.IntegerField(validators=[MinValueValidator(0)])

    def setEndDate(self):
        self.endDate = self.startDate + datetime.timedelta(days=self.durationInDays)

    def active(self):
        if self.endDate > datetime.date.today():
            if self.is_active==False:
                pass
            else:
                self.is_active=True
        else:
            self.is_active=False
            self.is_current=False
            self.is_completed=True

    def activate(self):
        self.startDate = datetime.date.today()
        self.is_active = True
        self.setEndDate()

    def deactivate(self):
        self.is_active = False
        self.is_current = False
        self.is_completed = True

    def hoursCompleted(self):
        hoursCompleted = 0
        tasks = self.task_set.all()
        for task in tasks:
            hoursCompleted+=task.hourSpent
        return hoursCompleted

    def hoursLeft(self):
        hoursDone = self.hoursCompleted()
        hoursLeft = self.totalEffortHours - hoursDone
        return hoursLeft



class Pbi(models.Model):
    STATUS_CHOICES=[
        ('Not Started(*)','Not Started(*)'),
        ('In Progress(*)','In Progress(*)'),
        ('Completed','Completed')
    ]
    title=models.CharField(max_length=200)
    projectID=models.ForeignKey(Project, on_delete=models.CASCADE)
    sprints=models.ManyToManyField(Sprint,blank=True)
    status=models.CharField(choices=STATUS_CHOICES, max_length=20, default='Not Started(*)')
    description=models.CharField(max_length=2000)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    storyPt=models.DecimalField(max_digits=2,decimal_places=0)
    teamID=models.CharField(max_length=2,default='A')
    class Meta:
        unique_together = (("title", "projectID"),)
    def __str__(self):
        return self.title
    def checkCompleted(self):
        tasks = self.task_set.all()
        if tasks.count() == 0:
            pass
        else:
            completed=True
            for task in tasks:
                if task.status != 'Completed':
                    completed=False
                    break
            if completed:
                self.status='Completed'
        self.save()


class Task(models.Model):
    STATUS_CHOICES=[
        ('Not Started','Not Started'),
        ('In Progress','In Progress'),
        ('Completed','Completed')
    ]

    pbi = models.ForeignKey(Pbi, on_delete=models.CASCADE)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    owner = models.ForeignKey(DevTeamMember,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    priority=models.DecimalField(max_digits=4,decimal_places=0)
    effortHours = models.IntegerField(validators=[MinValueValidator(0)])
    hourSpent=models.IntegerField(validators=[MinValueValidator(0)],blank=True, default=0)
    class Meta:
        unique_together = (("title", "pbi"),)

class InviteMessage(models.Model):
    receiver=models.ManyToManyField(User,blank = True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.project.projectID)
