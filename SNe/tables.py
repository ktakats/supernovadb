import django_tables2 as tables
from .models import Obs, Photometry

TEMPLATE='<a href="/sn/{{sn.id}}/obslog/edit/{{record.pk}}/" title="edit"><i class="fa fa-pencil"></i></a> <a href="#confirmmodal"  data-toggle="modal" data-id="{{record.pk}}" title="delete"><i class="fa fa-trash-o"></i></a>'


class ObsLogTable(tables.Table):
    obs_date=tables.DateColumn(short=True, verbose_name='Date')
    obs_type=tables.Column(verbose_name="Type")
    options=tables.TemplateColumn(TEMPLATE, orderable=False)

    class Meta:
        model=Obs
        exclude=('sn')

class PhotometryTable(tables.Table):

    class Meta:
        model=Photometry
        exclude=('sn')
