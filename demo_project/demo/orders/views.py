from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView
from django.forms import ModelForm
from .forms import *
from .models import Pbi
from .decorators import *
from django.http import HttpResponseRedirect
from django.contrib.auth import login

# Create your views here.

class HomePage(TemplateView):
    template_name = 'homepage.html'


@login_required
@prodowner_required
def addPbi(request,projectID):
    if request.method == "POST":
        form = PbiCreateForm(request.POST)
        if form.is_valid():
            newPbi = form.save(commit=False)
            newPbi.save()
            address='/'+projectID+'/main'
            return HttpResponseRedirect(address)
    else:
        form = PbiCreateForm()
    return render(request, 'CreatePbi.html',{'form':form})


class OnePbi(TemplateView):
    template_name="OnePbi.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        context['pbi']=Pbi_list.filter(title=target).first()
        return context

@login_required
@prodowner_required
def modifyPbi(request, projectID,target=None):
    item  = Pbi.objects.filter(title=target).first()
    address='../'+target
    form = PbiModifyForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(address)
    return render(request, 'ModifyPbi.html', {'form':form})

@login_required
@prodowner_required
def deletePbi(request, projectID,pk):

    trash=get_object_or_404(Pbi, pk=pk)
    if request.method=='POST':
        form=PbiCreateForm(request.POST,instance=trash)
        trash.delete()
        address='/'+projectID+'/main'
        return HttpResponseRedirect(address)
    else:
        form=PbiCreateForm(instance=trash)
    return render(request, 'delete.html',{'form':form})

class mainPage(TemplateView):
    template_name="main.html"
    def get_context_data(self, **kwargs):
        projectID=self.kwargs['projectID']
        context = super().get_context_data(**kwargs)

        pbiList=Pbi.objects.filter(projectID=projectID).order_by('-priority')

        context['pbi_list'] = pbiList
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
