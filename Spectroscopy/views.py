from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from SNe.models import SN
from .forms import UploadSpectrumForm
from .helpers import uploadSpectrum
from .models import Spectrum
from .tables import SpectroscopyTable

from simplejson import dumps
import math

from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/')
def spectroscopy(request, sn_id):
    sn = SN.objects.get(id=sn_id)
    sp = Spectrum.objects.filter(sn=sn)
    table = SpectroscopyTable(sp, order_by="id")
    if request.method == "POST":
        if request.FILES:
            form = UploadSpectrumForm(request.POST, request.FILES)
            if form.is_valid():
                # out returns -1 if the file is not correct
                uploadSpectrum(request.FILES['file'], sn, request.POST['MJD'], request.POST['notes'])
                # Sp=Spectrum.objects.filter(sn=sn)
                # table=SpectroscopyTable(Sp)
                return redirect(reverse('spectroscopy', args=(sn.id,)))
            else:
                return render(request, 'Spectroscopy/spectroscopy.html', {'sn': sn, 'uploadform': form, 'table': table})

    form = UploadSpectrumForm()
    return render(request, 'Spectroscopy/spectroscopy.html', {'sn': sn, 'uploadform': form, 'table': table})


@login_required(login_url='/')
def delSpectrum(request, sn_id):
    idlist = request.POST.getlist('idlist')[0].split(',')
    for myid in idlist:
        Spectrum.objects.filter(id=myid).delete()
    return redirect(reverse('spectroscopy', args=(sn_id,)))


@login_required(login_url='/')
def query(request, sn_id):
    idlist = request.GET.getlist('ids[]')
    sn = SN.objects.get(id=sn_id)
    if len(idlist) > 0:
        spectra = Spectrum.objects.filter(sn=sn, id__in=idlist)
    else:
        spectra = Spectrum.objects.filter(sn=sn)
    spdata = []
    for obj in spectra:
        wv=obj.wavelength
        flux = obj.flux
        spdata.append(
            {"MJD": obj.MJD, "spectrum": [{"wavelength": wv[p]/1000., "flux": flux[p]/1000.} for p in range(len(wv)) if not flux[p]==99999]})

    if sn.reference_date:
        try:
            refdate,refmode=sn.reference_date.encode('utf8').strip().split(" ")
            refdate=float(refdate)
            refmode=refmode.strip("(").strip(")")
        except ValueError:
            refdate=float(sn.reference_date.encode('utf8').strip())
            refmode=None
    else:
        refdate,refmode=None, None
    return HttpResponse(dumps({"data": spdata, "reference_date": refdate, "reference_mode": refmode}))
