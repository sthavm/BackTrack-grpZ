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
from django.contrib.auth import login

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
            address='/'+projectID+'/main'
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
            request.user.save()
            productOwner = ProductOwner.objects.create(user=request.user)
            productOwner.project = newProject
            productOwner.save()
            projectID = newProject.projectID
            address='/'+projectID+'/main'
            return HttpResponseRedirect(address)
    else:
        form = CreateProjectForm()
    return render(request, 'CreateProject.html',{'form':form})


class OnePbi(TemplateView):
    template_name="OnePbi.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        projectID=self.kwargs['projectID']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        context['pbi']=Pbi_list.filter(title=target).filter(projectID=projectID).first()
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
def modifyTask(request, projectID, target=None):
    item  = Task.objects.filter(title=target).first()
    address='../'+target
    form = TaskModifyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(address)
    return render(request, 'ModifyTask.html', {'form':form})

@login_required
@prodowner_required
def deletePbi(request,projectID, pk):

    trash=get_object_or_404(Pbi, title=pk)
    if request.method=='POST':
        form=PbiCreateForm(request.POST,instance=trash)
        trash.delete()
        address='/'+projectID+'/main'
        return HttpResponseRedirect(address)
    else:
        form=PbiCreateForm(instance=trash)
    return render(request, 'delete.html',{'form':form})

class AllProjects(ListView):
    model = Project
    template_name = "allprojects.html"
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class mainPage(TemplateView):
    template_name="main.html"
    def get_context_data(self, **kwargs):
        projectID=self.kwargs['projectID']
        context = super().get_context_data(**kwargs)
        project=Project.objects.filter(projectID=projectID).first()
        pbiList=Pbi.objects.filter(projectID=projectID).order_by('-priority')
        sprintList=Sprint.objects.filter(project=projectID).order_by('sprintNumber')
        cumsumList=[]
        cumsum=0
        for i in range (len(pbiList)):
            cumsum+=pbiList[len(pbiList)-1-i].storyPt
            cumsumList.append(int(cumsum))
        cumsumList.reverse()
        zipped=zip(pbiList, cumsumList)
        context['pbi_list'] = zipped
        context['sprintList']=sprintList
        context['project']=project
        return context


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class NoProjectView(TemplateView):
    template_name = 'noproject.html'

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
@prodowner_required
def CreateSprint(request,projectID):
    if hasActiveSprint(request.user.productowner.project):
        messages.info(request, 'ALERT: There is already an active sprint in this project')
        raise PermissionDenied()
        address='/'+projectID+'/main'
        return HttpResponseRedirect(address)
    else:
        if request.method == "POST":
            form = CreateSprintForm(request.POST)
            if form.is_valid():
                newSprint = form.save(commit=False)
                newSprint.project=request.user.productowner.project
                newSprint.setEndDate()
                newSprint.is_active=True
                newSprint.save()
                address='/'+projectID+'/main'
                return HttpResponseRedirect(address)
        else:
            form = CreateSprintForm()
        return render(request, 'CreateSprint.html',{'form':form})

@login_required
@dev_required
def CreateTask(request,projectID):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            newTask = form.save(commit=False)
            newTask.creator=request.user.developmentteammember
            newTask.status='Not Started'
            newTask.save()
            address='/'+projectID+'/main'
            return HttpResponseRedirect(address)
    else:
        form = CreateTaskForm()
    return render(request, 'CreateTask.html',{'form':form})


@login_required
def redir(request):
    currentUser = request.user
    isManager = currentUser.is_manager
    isDev = currentUser.is_devteam
    isProdOwn = currentUser.is_prodowner
    if (isManager):
        return redirect('/projects')
    elif (isDev):
        if (currentUser.devteammember.project == None):
            return redirect('/noproject')
        else:
            projectID = currentUser.devteammember.project.projectID
            address='/'+projectID+'/main'
            return redirect(address)
    elif (isProdOwn):
        projectID = currentUser.productowner.project.projectID
        address='/'+projectID+'/main'
        return redirect(address)

def hasActiveSprint(Project):
    sprints=Project.sprint_set.all()
    for sprint in sprints:
        if sprint.active == True:
            return True
    return False
