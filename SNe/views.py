from django.shortcuts import redirect, render
from models import SN

# Create your views here.

def home(request):
    return render(request, 'home.html')

def add_sn(request):
    if request.method=='POST':
        sn=SN.objects.create(sn_name=request.POST['new_sn'])
        return redirect(sn)
    else:
        return render(request, 'new_sn.html')

def view_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    return render(request, 'sn.html', {'sn': sn.sn_name})
