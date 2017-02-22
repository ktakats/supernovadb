from django.shortcuts import render
from SNe.models import SN
from .models import Photometry
from .forms import PhotometryForm, UploadPhotometryFileForm
from .tables import PhotometryTable
from helpers import uploadPhotometry

# Create your views here.
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
