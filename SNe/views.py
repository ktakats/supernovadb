from django.shortcuts import redirect, render, get_object_or_404
from models import SN, Obs
from Photometry.models import Photometry
from forms import NewSNForm, ObsLogForm, PhotometryForm, UploadPhotometryFileForm
from tables import ObsLogTable, PhotometryTable
from django_tables2 import RequestConfig
from astropy.coordinates import SkyCoord
from astropy import units as u
from helpers import uploadPhotometry
from django.forms.utils import ErrorList

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

def photometry(request, sn_id, phot_id=None):
    sn=SN.objects.get(id=sn_id)
    out=1
    if request.method=="POST":
        if request.FILES:
            form=UploadPhotometryFileForm(request.POST, request.FILES)
            if form.is_valid():
                out=uploadPhotometry(request.FILES['file'], sn)
                #out returns -1 if the file is not correct

        else:
            form=PhotometryForm(request.POST)
            if form.is_valid():
                form.save(sn=sn, id=phot_id)
    try:
        instance=Photometry.objects.get(id=phot_id)
    except Photometry.DoesNotExist:
        instance=None
    form=PhotometryForm(instance=instance)
    uploadform=UploadPhotometryFileForm()
    if out==-1:
        errors=uploadform.errors.setdefault("file", ErrorList())
        errors.append(u"The file format is incorrect. Please check the requirements.")

    phot=Photometry.objects.filter(sn=sn)
    table=PhotometryTable(phot)
    RequestConfig(request).configure(table)
    return render(request, 'photometry.html', {'sn': sn, 'form': form, 'uploadform': uploadform, 'table': table})

def deletePhot(request, sn_id, phot_id):
    sn=SN.objects.get(id=sn_id)
    Photometry.objects.filter(id=phot_id).delete()
    form=PhotometryForm()
    uploadform=UploadPhotometryFileForm()
    phot=Photometry.objects.filter(sn=sn)
    table=PhotometryTable(phot)
    RequestConfig(request).configure(table)
    return render(request, 'photometry.html', {'sn': sn, 'form': form, 'uploadform': uploadform, 'table': table})
