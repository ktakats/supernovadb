from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404, reverse

from models import SN, Project
from forms import NewSNForm, AddCoIForm, NewProjectForm
from accounts.forms import LoginForm

from astropy import units as u
from astropy.coordinates import SkyCoord

from django_tables2 import RequestConfig


User=auth.get_user_model()


# Create your views here.
def home(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        email=request.POST['email']
        password=request.POST['password']
        if form.is_valid():
            user=authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('my_stuff'))
    else:
        form=LoginForm()
    return render(request, 'home.html', {'form': form})

@login_required(login_url='/')
def add_sn(request):
    if request.method=='POST':
        form=NewSNForm(data=request.POST)
        if form.is_valid():
            sn=form.save(request.user)
            return redirect(sn.get_absolute_url())
        else:
            return render(request, 'new_sn.html', {'form': form})
    else:
        form=NewSNForm()
        return render(request, 'new_sn.html', {'form':form})

@login_required(login_url='/')
def view_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    if request.method=='POST':
        addcoiform=AddCoIForm(request.POST, instance=sn)
        if addcoiform.is_valid():
            sn.coinvestigators.add(request.POST['coinvestigators'])
            sn.save()

    c=SkyCoord(str(sn.ra), str(sn.dec), unit=u.degree)
    ra='%02d:%02d:%02.3f' % (c.ra.hms.h, abs(c.ra.hms.m), abs(c.ra.hms.s))
    dec='%02d:%02d:%02.2f' % (c.dec.dms.d, abs(c.dec.dms.m), abs(c.dec.dms.s))
    addcoiform=AddCoIForm(instance=sn)
    return render(request, 'sn.html', {'sn': sn, 'ra': ra, 'dec': dec, 'addcoiform': addcoiform})

@login_required(login_url='/')
def my_stuff(request):
    sne=SN.objects.filter(Q(pi=request.user) | Q(coinvestigators=request.user)).distinct()
    projects=Project.objects.filter(Q(pi=request.user) | Q(coinvestigators=request.user)).distinct()
    return render(request, 'my_stuff.html', {'sne': sne, 'projects': projects})

@login_required(login_url="/")
def add_project(request):
    if request.method=="POST":
        form=NewProjectForm(request.POST, instance=request.user)
        if form.is_valid():
            project=form.save()
            return redirect(project.get_absolute_url())
    form=NewProjectForm(instance=request.user)
    return render(request, 'new_project.html', {'form': form})

def view_project(request, project_id):
    project=Project.objects.get(id=project_id)
    return render(request, 'project.html', {'project': project})
