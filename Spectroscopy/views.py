from django.shortcuts import render
from SNe.models import SN

# Create your views here.

def spectroscopy(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    return render(request, 'spectroscopy.html', {'sn': sn})
