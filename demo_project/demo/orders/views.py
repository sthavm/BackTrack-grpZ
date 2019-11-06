from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.forms import ModelForm
from .forms import PbiForm
from .models import Pbi
from django.http import HttpResponseRedirect

# Create your views here.
class AllPbis(TemplateView):
    template_name = "AllPbis.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pbiList = Pbi.objects.order_by('-priority')
        context['pbi_list'] = pbiList
        return context


def addPbi(request):
    if request.method == "POST":
        form = PbiForm(request.POST)
        if form.is_valid():
            newPbi = form.save(commit=False)
            newPbi.save()
            return HttpResponseRedirect('/pbi')
    else:
        form = PbiForm()
    return render(request, 'CreatePbi.html',{'form':form})


class OnePbi(TemplateView):
    template_name="OnePbi.html"

    def get_context_data(self, **kwargs):
        target=self.kwargs['target']
        context=super().get_context_data(**kwargs)
        Pbi_list=Pbi.objects.all()
        context['pbi']=Pbi_list.filter(title=target).first()
        return context

def modifyPbi(request, target=None):
    item  = Pbi.objects.filter(title=target).first()
    address='../'+target
    form = PbiForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(address)
    return render(request, 'ModifyPbi.html', {'form':form})

def deletePbi(request, pk):

    trash=get_object_or_404(Pbi, pk=pk)
    if request.method=='POST':
        form=PbiForm(request.POST,instance=trash)
        trash.delete()
        return HttpResponseRedirect('/pbi')
    else:
        form=PbiForm(instance=trash)
    return render(request, 'delete.html',{'form':form})

class mainPage(TemplateView):
    template_name="main.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pbiList = Pbi.objects.order_by('-priority')
        context['pbi_list'] = pbiList
        return context
