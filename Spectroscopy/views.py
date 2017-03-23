from django.shortcuts import render, redirect, reverse
from SNe.models import SN
from .forms import UploadSpectrumForm
from .helpers import uploadSpectrum

# Create your views here.

def spectroscopy(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    if request.method=="POST":
        if request.FILES:
            form=UploadSpectrumForm(request.POST, request.FILES)
            if form.is_valid():
                #out returns -1 if the file is not correct
                out=uploadSpectrum(request.FILES['file'], request.POST['MJD'], sn)
                return redirect(reverse('spectroscopy', args=(sn.id,)), {'sn': sn, 'form': form, 'uploadform': form})

    form=UploadSpectrumForm()
    return render(request, 'spectroscopy.html', {'sn': sn, 'uploadform': form})
