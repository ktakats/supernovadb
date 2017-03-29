from django.shortcuts import redirect, render, get_object_or_404
from models import SN
from forms import NewSNForm
from accounts.forms import LoginForm
from django_tables2 import RequestConfig
from astropy.coordinates import SkyCoord
from astropy import units as u
from django.contrib.auth import authenticate, login
from django.contrib import auth

User=auth.get_user_model()


# Create your views here.
def home(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        email=request.POST['username']
        password=request.POST['password']
        if form.is_valid():
            user=authenticate(username=email, password=password)
            if user:
                login(request, user)
    else:
        form=LoginForm()
    return render(request, 'home.html', {'form': form})

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

def view_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    c=SkyCoord(str(sn.ra), str(sn.dec), unit=u.degree)
    ra='%02d:%02d:%02.3f' % (c.ra.hms.h, c.ra.hms.m, c.ra.hms.s)
    dec='%02d:%02d:%02.2f' % (c.dec.dms.d, c.dec.dms.m, c.dec.dms.s)
    return render(request, 'sn.html', {'sn': sn, 'ra': ra, 'dec': dec})
