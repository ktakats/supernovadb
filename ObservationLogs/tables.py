import django_tables2 as tables
from ObservationLogs.models import Obs
from Photometry.models import Photometry

TEMPLATE_EDITOBS='<a href="/sn/{{sn.id}}/obslog/edit/{{record.pk}}/" title="edit"><i class="fa fa-pencil"></i></a> <a href="#confirmmodal"  data-toggle="modal" data-id="{{record.pk}}" title="delete"><i class="fa fa-trash-o"></i></a>'



class ObsLogTable(tables.Table):
    obs_date=tables.DateColumn(short=True, verbose_name='Date')
    obs_type=tables.Column(verbose_name="Type")
    options=tables.TemplateColumn(TEMPLATE_EDITOBS, orderable=False)

    class Meta:
        model=Obs
        exclude=('sn', 'id')
