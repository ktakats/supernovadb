from django.shortcuts import render, redirect, reverse
from django.forms.utils import ErrorList
from django_tables2 import RequestConfig
from SNe.models import SN
from .models import Photometry
from .forms import PhotometryForm, UploadPhotometryFileForm
from .tables import PhotometryTable
from helpers import uploadPhotometry
import simplejson as json
#helper functions
from django.http import HttpResponse

def render_photometry_page(request, sn, form, out=1):
    uploadform=UploadPhotometryFileForm()
    #if the file upload was unsuccessful, i.e. out==-1, attach an error to the form

    if out==-1:
        errors=uploadform.errors.setdefault("file", ErrorList())
        errors.append(u"The file format is incorrect. Please check the requirements.")
    phot=Photometry.objects.filter(sn=sn)
    table=PhotometryTable(phot)
    RequestConfig(request).configure(table)
    if request.method=="POST" and not uploadform.errors:
        return redirect(reverse('photometry', args=(sn.id,)), {'sn': sn, 'form': form, 'uploadform': uploadform, 'table': table})

    return render(request, 'photometry.html', {'sn': sn, 'form': form, 'uploadform': uploadform, 'table': table})

# Create your views here.
def photometry(request, sn_id, phot_id=None):
    sn=SN.objects.get(id=sn_id)
    out=1
    if request.method=="POST":
        #if the user uploaded a file
        if request.FILES:
            form=UploadPhotometryFileForm(request.POST, request.FILES)
            if form.is_valid():
                #out returns -1 if the file is not correct
                out=uploadPhotometry(request.FILES['file'], sn)


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

    return render_photometry_page(request, sn, form, out)

def deletePhot(request, sn_id, phot_id):
    sn=SN.objects.get(id=sn_id)
    Photometry.objects.filter(id=phot_id).delete()
    form=PhotometryForm()
    return render_photometry_page(request, sn, form)

def queryPhot(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    phot=Photometry.objects.filter(sn=sn)
    photdata=[obj.as_dict() for obj in phot]
    return HttpResponse(json.dumps({"data": photdata}))
