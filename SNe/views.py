from django.shortcuts import redirect, render, get_object_or_404
from models import SN
from forms import NewSNForm, AddCoIForm
from accounts.forms import LoginForm
from django_tables2 import RequestConfig
from astropy.coordinates import SkyCoord
from astropy import units as u
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Q

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
    else:
        form=LoginForm()
    return render(request, 'home.html', {'form': form})

@login_required(login_url='/')
def add_sn(request):
    if request.method=='POST':
        form=NewSNForm(data=request.POST)
        if form.is_valid():
            sn=form.save(request.user)
            return redirect(sn)
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
    ra='%02d:%02d:%02.3f' % (c.ra.hms.h, c.ra.hms.m, c.ra.hms.s)
    dec='%02d:%02d:%02.2f' % (c.dec.dms.d, c.dec.dms.m, c.dec.dms.s)
    addcoiform=AddCoIForm(instance=sn)
    return render(request, 'sn.html', {'sn': sn, 'ra': ra, 'dec': dec, 'addcoiform': addcoiform})

@login_required(login_url='/')
def my_sne(request):
    sne=SN.objects.filter(Q(pi=request.user) | Q(coinvestigators=request.user))
    return render(request, 'my_sne.html', {'sne': sne})

def add_project(request):
    return render(request, 'new_project.html')
