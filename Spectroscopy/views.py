from django.shortcuts import render
from SNe.models import SN
from .forms import UploadSpectrumForm

# Create your views here.

def spectroscopy(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    form=UploadSpectrumForm()
    return render(request, 'spectroscopy.html', {'sn': sn, 'uploadform': form})
