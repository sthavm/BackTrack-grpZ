from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, ListView
from django.forms import ModelForm
from .forms import *
from .models import *
from .decorators import *
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout

# Create your views here.

class HomePage(TemplateView):
    template_name = 'homepage.html'


class AllPbis(TemplateView):
    template_name = "AllPbis.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pbiList = Pbi.objects.order_by('-priority')
        context['pbi_list'] = pbiList
        return context

@login_required
@prodowner_required
def addPbi(request,projectID):
    if request.method == "POST":
        form = PbiCreateForm(request.POST)
        if form.is_valid():
            newPbi = form.save(commit=False)
            newPbi.projectID=request.user.productowner.project
            newPbi.save()
            address='/'+str(projectID)+'/main'
            return HttpResponseRedirect(address)
    else:
        form = PbiCreateForm()
    return render(request, 'CreatePbi.html',{'form':form})

@login_required
@dev_required
def createProject(request):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            newProject = form.save(commit=False)
            newProject.save()
            request.user.is_devteam = False
            request.user.is_prodowner = True
            request.user.is_available=False
            request.user.devteammember.delete()
            request.user.save()
            productOwner = ProductOwner.objects.create(user=request.user)
            productOwner.project = newProject
            productOwner.save()
            projectID = newProject.projectID
            address='/'+str(projectID)+'/main/create-invite'
            messages.info(request, 'You now become a Product Owner!')
            return HttpResponseRedirect(address)
    else:
        form = CreateProjectForm()
    return render(request, 'CreateProject.html',{'form':form})

def AcceptInviteLanding(request,projectID):
    request.user.devteammember.project = Project.objects.filter(projectID=projectID).first()
    request.user.devteammember.save()
    return HttpResponseRedirect('/'+projectID+'/main')



class OnePbi(TemplateView):
    template_name="OnePbi.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        projectID=self.kwargs['projectID']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        context['pbi']=Pbi_list.filter(title=target).filter(projectID=projectID).first()
        return context
class OneTask(TemplateView):
    template_name="OneTask.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        projectID=self.kwargs['projectID']
        pbiTitle=self.kwargs['pbi']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        pbi=Pbi_list.filter(title=pbiTitle).filter(projectID=projectID).first()
        task=Task.objects.filter(pbi=pbi).get(title=target)
        context['task']=task
        return context

@login_required
@dev_required
def TakeOwnership(request, projectID,pbi,target):
        Pbi_list=Pbi.objects.all()
        PBI=Pbi_list.filter(title=pbi).filter(projectID=projectID).first()
        task=Task.objects.filter(pbi=PBI).get(title=target)
        if task.owner==None:
            task.owner=request.user.devteammember
            task.save()
            address='/'+str(projectID)+'/main/'+pbi+'/task/'+target
            return HttpResponseRedirect(address)
        else:
            messages.info(request, 'The Task Has Owner Already')
            address='/'+str(projectID)+'/main/'+pbi+'/task/'+target
            return HttpResponseRedirect(address)
@login_required
@dev_required
def GiveUpOwnership(request, projectID,pbi,target):
        Pbi_list=Pbi.objects.all()
        PBI=Pbi_list.filter(title=pbi).filter(projectID=projectID).first()
        task=Task.objects.filter(pbi=PBI).get(title=target)
        if task.owner==request.user.devteammember:
            task.owner=None
            task.save()
            address='/'+str(projectID)+'/main/'+pbi+'/task/'+target
            return HttpResponseRedirect(address)
        else:
            messages.info(request, 'You Are Not The Owner')
            address='/'+str(projectID)+'/main/'+pbi+'/task/'+target
            return HttpResponseRedirect(address)



class CurrentPbi(TemplateView):
    template_name="currentPbi.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        projectID=self.kwargs['projectID']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        pbi=Pbi_list.filter(title=target).filter(projectID=projectID).first()
        sprints=pbi.sprints.all()
        sprintNum=[]
        for s in sprints:
            sprintNum.append(s.sprintNumber)
        context['sprintNum']=sprintNum
        context['pbi']=pbi
        return context

@login_required
@prodowner_required
def modifyPbi(request, projectID, target=None):
    item  = Pbi.objects.filter(title=target).first()
    address='../'+target
    form = PbiModifyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(address)
    return render(request, 'ModifyPbi.html', {'form':form})

@login_required
@dev_required
def modifyTask(request, projectID, pbi,target=None):
    item  = Task.objects.filter(title=target).first()
    address='/'+str(projectID)+'/main'
    form = TaskModifyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(address)
    return render(request, 'ModifyTask.html', {'form':form})

@login_required
@prodowner_required
def deletePbi(request,projectID, pk):
    pbis=Pbi.objects.filter(projectID=projectID)
    trash=pbis.get(title=pk)
    if request.method=='POST':
        form=PbiCreateForm(request.POST,instance=trash)
        trash.delete()
        address='/'+str(projectID)+'/main'
        return HttpResponseRedirect(address)
    else:
        form=PbiCreateForm(instance=trash)
    return render(request, 'delete.html',{'form':form})

def deleteTask(request,projectID, pbi, target):
    sprints=Sprint.objects.filter(project=projectID)
    tmp=Pbi.objects.filter(projectID=projectID).get(title=pbi)
    task=Task.objects.filter(pbi=tmp).filter(title=target)
    task.delete()
    address='/'+str(projectID)+'/main'
    return HttpResponseRedirect(address)
#manager's projects
class AllProjects(ListView):
    model = Project
    template_name = "allprojects.html"
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project=self.request.user.manager.project
        context['project']=project.all()
        context['now'] = timezone.now()
        return context

class allSprint(TemplateView):
    template_name="AllSprint.html"
    def get_context_data(self, **kwargs):
        projectID=self.kwargs['projectID']
        context = super().get_context_data(**kwargs)
        sprintList=Sprint.objects.filter(project=projectID).order_by('sprintNumber')
        pbiList=Pbi.objects.filter(sprints__in=sprintList)
        mapping=[]
        for s in sprintList:
            for p in pbiList:
                tmp=(s,p, Pbi.objects.filter(pk=p.pk).filter(sprints=s).exists())
                mapping.append(tmp)
        taskList=Task.objects.filter(pbi__in=pbiList)
        taskDone=taskList.filter(status="Completed")
        taskProgress=taskList.filter(status="In Progress")
        taskNot=taskList.filter(status="Not Started")
        #time tracking##########################################
        myTask=taskList.filter(owner=self.request.user.devteammember)
        sumEstimatedHour=0
        sumAcutalHour=0
        for t in myTask:
            sumEstimatedHour+=t.effortHours
            if t.hourSpent==None:
                continue
            else:
                sumActualHour+=t.hourSpent
        context['sumEHour']=sumEstimatedHour
        context['sumAHour']=sumAcutalHour
        if self.request.user.is_devteam:
            context['devteam']=True
        else:
            context['devteam']=False
        #################################################
        context['sprintList']=sprintList
        context['pbiList']=pbiList
        context['taskDone']=taskDone
        context['taskProgress']=taskProgress
        context['taskNot']=taskNot
        context['mapping']=mapping
        print(mapping)
        return context

class mainPage(TemplateView):
    template_name="main.html"
    def get_context_data(self, **kwargs):
        projectID=self.kwargs['projectID']
        context = super().get_context_data(**kwargs)
        project=Project.objects.filter(projectID=projectID).first()
        pbiList=Pbi.objects.filter(projectID=projectID).order_by('-priority')
        currentSprint=Sprint.objects.filter(project=projectID).filter(is_active=True).first()
        if currentSprint==None:
            currentPbiList=[]
        else:
            currentPbiList=Pbi.objects.filter(sprints=currentSprint)
        taskList=Task.objects.filter(pbi__in=currentPbiList)
        taskDone=taskList.filter(status="Completed")
        taskProgress=taskList.filter(status="In Progress")
        taskNot=taskList.filter(status="Not Started")
        #time tracking##########################################
        if self.request.user.is_devteam:
            myTask=taskList.filter(owner=self.request.user.devteammember)
            sumEstimatedHour=0
            sumAcutalHour=0
            for t in myTask:
                sumEstimatedHour+=t.effortHours
                if t.hourSpent==None:
                    continue
                else:
                    sumActualHour+=t.hourSpent
            context['sumEHour']=sumEstimatedHour
            context['sumAHour']=sumAcutalHour
            if self.request.user.is_devteam:
                context['devteam']=True
            else:
                context['devteam']=False
        #################################################
        cumsumList=[]
        cumsum=0
        for i in range (len(pbiList)):
            cumsum+=pbiList[i].storyPt
            cumsumList.append(int(cumsum))
        zipped=zip(pbiList, cumsumList)
        if self.request.user.is_prodowner:
            context['prodowner']=True
        else:
            context['prodowner']=False
        context['pbi_list'] = zipped
        context['currentSprint']=currentSprint
        context['project']=project

        context['currentPbiList']=currentPbiList

        context['taskDone']=taskDone
        context['Completed']="Completed"

        context['taskProgress']=taskProgress
        context['InProgess']="In Progress"

        context['taskNot']=taskNot
        context['NotStarted']="Not Started"
        return context


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class NoProjectView(TemplateView):
    template_name = 'noproject.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        currentUser = self.request.user
        distinctProjects=[]
        distinctInvites=[]
        relatedInvites = currentUser.invitemessage_set.all()
        for invite in relatedInvites:
            if invite.project not in distinctProjects:
                distinctProjects.append(invite.project)
                distinctInvites.append(invite)
        context['invites']=distinctInvites
        context['hello']="Hello there"
        return context

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/redir')


class DevSignUpView(CreateView):
    model = User
    form_class = DevSignUpForm
    template_name = 'registration/signup_form.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'dev'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
       user = form.save()
       login(self.request, user)
       return redirect('/redir')

@login_required
@dev_required
def CreateSprint(request,projectID):
        if request.method == "POST":
            form = CreateSprintForm(request.POST)
            if form.is_valid():
                newSprint = form.save(commit=False)
                newSprint.project=request.user.productowner.project
                newSprint.setEndDate()
                newSprint.is_active=True
                newSprint.save()
                address='/'+str(projectID)+'/main'
                return HttpResponseRedirect(address)
        else:
            form = CreateSprintForm()
        return render(request, 'CreateSprint.html',{'form':form})

@login_required
@dev_required
def CreateTask(request,projectID,target):
    sprints=Sprint.objects.filter(project=projectID)
    pbi=Pbi.objects.filter(projectID=projectID).get(title=target)
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            newTask = form.save(commit=False)
            newTask.status='Not Started'
            newTask.pbi=pbi
            newTask.save()
            p=newTask.pbi
            address='/'+str(projectID)+'/main'
            return HttpResponseRedirect(address)
    else:
        form = CreateTaskForm()
    return render(request, 'CreateTask.html',{'form':form})

def CreateSprintLanding(request,projectID):
    sprints=request.user.productowner.project.sprint_set.all()
    hasActiveSprint=False
    for sprint in sprints:
        sprint.active()
        if sprint.is_active == True:
            hasActiveSprint = True
            break
        else:
            hasActiveSprint = False

    if hasActiveSprint:
            address='/'+str(projectID)+'/main'
            messages.info(request, 'Project has Active Sprint already!')
            return HttpResponseRedirect(address)
    else:
        return HttpResponseRedirect('/'+projectID+'/main/createSprint')

@login_required
@prodowner_required
def SendInvite(request,projectID):
    currentUser = request.user
    project = currentUser.productowner.project
    if request.method == "POST":
        form = CreateInviteForm(request.POST)
        if form.is_valid():
            newInvite = form.save(commit=False)
            newInvite.project=project
            newInvite.save()
            form.save_m2m()
            address='/'+str(projectID)+'/main'
            return HttpResponseRedirect(address)
    else:
        form = CreateInviteForm()
    return render(request, 'SendInvite.html',{'form':form})


def BringPbiToSprint(request,projectID,target):
    sprints=Sprint.objects.filter(project=projectID)
    pbi=Pbi.objects.filter(projectID=projectID).get(title=target)
    for s in sprints:
        if s.is_active == True:
            allCPbi=s.pbi_set.all()
            for p in allCPbi:
                if p==pbi:
                    messages.info(request, 'Same PBI Cannot be Added Again')
                    return HttpResponseRedirect('/'+projectID+'/main/'+'pbi/'+target)
            pbi.status="In Progress"
            pbi.save()
            pbi.sprints.add(s)
            address='/'+str(projectID)+'/main'
            return HttpResponseRedirect(address)
    messages.info(request, 'No Active Sprint')
    return HttpResponseRedirect('/'+projectID+'/main/'+'pbi/'+target)

def RemoveCurrentPbi(request, projectID,target):
    sprints=Sprint.objects.filter(project=projectID)
    pbi=Pbi.objects.filter(projectID=projectID).get(title=target)
    for s in sprints:
        if s.is_active == True:
            pbi.sprints.remove(s)
            address='/'+str(projectID)+'/main'
            return HttpResponseRedirect(address)

@login_required
def redir(request):
    currentUser = request.user
    isManager = currentUser.is_manager
    isDev = currentUser.is_devteam
    isProdOwn = currentUser.is_prodowner
    if (isManager):
        messages.info(request, 'You are a Manager!')
        return redirect('/projects')
    elif (isDev):
        if (currentUser.devteammember.project == None):
            messages.info(request, 'You are a Developer!')
            return redirect('/noproject')
        else:
            projectID = currentUser.devteammember.project.projectID
            address='/'+str(projectID)+'/main'
            messages.info(request, 'You are a Developer!')
            return redirect(address)
    elif (isProdOwn):
        projectID = currentUser.productowner.project.projectID
        address='/'+str(projectID)+'/main'
        messages.info(request, 'You are a Product Owner!')
        return redirect(address)

def logout_view(request):
    logout(request)
    return redirect('/')
