from django.shortcuts import render
from django_tables2 import RequestConfig
from ObservationLogs.forms import ObsLogForm
from ObservationLogs.models import Obs
from ObservationLogs.tables import ObsLogTable
from SNe.models import SN

#Helper functions
def render_obslog_page(sn, request, form):
    obs=Obs.objects.filter(sn=sn)
    table=ObsLogTable(obs)
    RequestConfig(request).configure(table)

    return render(request, 'obslog.html', {'sn': sn, 'form': form, 'table': table})


# Create your views here.
def view_obslog(request, sn_id, obs_id=None):
    sn=SN.objects.get(id=sn_id)
    try:
        instance=Obs.objects.get(id=obs_id)
    except Obs.DoesNotExist:
        instance=None
    form=ObsLogForm(request.POST or None, instance=instance)
    if request.method=='POST':
        if form.is_valid():
            form.save(sn=sn, id=obs_id)

    return render_obslog_page(sn, request, form)

def deleteobs(request, sn_id, obs_id):
    sn=SN.objects.get(id=sn_id)
    Obs.objects.filter(id=obs_id).delete()
    form=ObsLogForm()
    return render_obslog_page(sn, request, form)
