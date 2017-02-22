from django.shortcuts import redirect, render, get_object_or_404
from models import SN
from forms import NewSNForm
from django_tables2 import RequestConfig
from astropy.coordinates import SkyCoord
from astropy import units as u



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
