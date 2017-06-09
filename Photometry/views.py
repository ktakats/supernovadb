from django.shortcuts import render, redirect, reverse
from django.forms.utils import ErrorList
from django_tables2 import RequestConfig
from SNe.models import SN
from Spectroscopy.models import Spectrum
from .models import Photometry
from .forms import PhotometryForm, UploadPhotometryFileForm
from .tables import PhotometryTable
from helpers import uploadPhotometry
import simplejson as json
#helper functions
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def render_photometry_page(request, sn, form, uploadform=None, out=1,):
    if uploadform==None:
        uploadform=UploadPhotometryFileForm()
    #if the file upload was unsuccessful, i.e. out==-1, attach an error to the form

    if out==-1:
        errors=uploadform.errors.setdefault("file", ErrorList())
        errors.append(u"The file format is incorrect. Please check the requirements.")
    phot=Photometry.objects.filter(sn=sn)
    table=PhotometryTable(phot)
    RequestConfig(request).configure(table)
    if request.method=="POST" and not uploadform.errors:
        return redirect(reverse('photometry', args=(sn.id,)))

    return render(request, 'Photometry/photometry.html', {'sn': sn, 'form': form, 'uploadform': uploadform, 'table': table})

# Create your views here.
@login_required(login_url="/")
def photometry(request, sn_id, phot_id=None):
    sn=SN.objects.get(id=sn_id)
    out=1
    if request.method=="POST":
        #if the user uploaded a file
        if request.FILES:
            uploadform=UploadPhotometryFileForm(request.POST, request.FILES)

            if uploadform.is_valid():
                #out returns -1 if the file is not correct
                out=uploadPhotometry(request.FILES['file'], sn)
            else:
                form=PhotometryForm()
                return render_photometry_page(request, sn, form, uploadform=uploadform, out=out)


        #if the user submited the form
        else:
            form=PhotometryForm(request.POST)
            if form.is_valid():
                form.save(sn=sn, id=phot_id)
    #if the GET request is an edit request, find entry
    try:
        instance=Photometry.objects.get(id=phot_id)
    except Photometry.DoesNotExist:
        instance=None
    form=PhotometryForm(instance=instance)

    return render_photometry_page(request, sn, form, out=out)

@login_required(login_url="/")
def deletePhot(request, sn_id):
    photlist=request.POST.getlist('idlist')[0].split(',')
    sn=SN.objects.get(id=sn_id)
    for id in photlist:
        Photometry.objects.filter(id=id).delete()
    form=PhotometryForm()
    return render_photometry_page(request, sn, form)

@login_required(login_url="/")
def queryPhot(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    phot=Photometry.objects.filter(sn=sn)
    photdata=[obj.as_dict() for obj in phot]
    #get spectra of the SN
    sp=Spectrum.objects.filter(sn=sn)
    spdata=[obj.as_dict() for obj in sp]
    #get reference date and mode if exsists
    if sn.reference_date:
        try:
            refdate, refmode=sn.reference_date.encode('utf8').strip().split(" ")
            refdate = float(refdate)
            refmode = refmode.strip("(").strip(")")
        except:
            refdate=float(sn.reference_date.encode('utf8').strip())
            refmode=None

    else:
        refmode, refdate=None, None
    return HttpResponse(json.dumps({"data": photdata, "reference_date": refdate, "reference_mode": refmode, 'spectra': spdata}))
