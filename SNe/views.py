from django.shortcuts import redirect, render, get_object_or_404
from models import SN, Obs
from forms import NewSNForm, ObsLogForm
from tables import ObsLogTable
from django_tables2 import RequestConfig
from astropy.coordinates import SkyCoord
from astropy import units as u

#Helper functions
def render_obslog_page(sn, request, form):
    obs=Obs.objects.filter(sn=sn)
    table=ObsLogTable(obs)
    RequestConfig(request).configure(table)

    return render(request, 'obslog.html', {'sn': sn, 'form': form, 'table': table})


# Create your views here.
def home(request):
    return render(request, 'home.html')

def add_sn(request):
    if request.method=='POST':
        form=NewSNForm(data=request.POST)
        if form.is_valid():
            sn=form.save()
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

def view_obslog(request, sn_id, obs_id=None):
    sn=SN.objects.get(id=sn_id)
    try:
        instance=Obs.objects.get(id=obs_id)
    except Obs.DoesNotExist:
        instance=None
    form=ObsLogForm(request.POST or None, instance=instance)
    if request.method=='POST':
        if form.is_valid():
            form.save(sn=sn, id=obs_id)

    return render_obslog_page(sn, request, form)

def deleteobs(request, sn_id, obs_id):
    sn=SN.objects.get(id=sn_id)
    Obs.objects.filter(id=obs_id).delete()
    form=ObsLogForm()
    return render_obslog_page(sn, request, form)
