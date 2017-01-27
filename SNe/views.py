from django.shortcuts import redirect, render
from models import SN
from forms import NewSNForm

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
        form=NewSNForm()
        return render(request, 'new_sn.html', {'form':form})

def view_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    return render(request, 'sn.html', {'sn': sn.sn_name})
