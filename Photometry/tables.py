import django_tables2 as tables
from .models import Photometry

TEMPLATE_EDITPHOT='<a href="/sn/{{sn.id}}/photometry/edit/{{record.pk}}/" title="edit"><i class="fa fa-pencil"></i></a> <a href="#confirmmodal"  data-toggle="modal" data-id="{{record.pk}}" title="delete"><i class="fa fa-trash-o"></i></a>'

class PhotometryTable(tables.Table):
    mag_error=tables.Column(verbose_name="Error")
    options=tables.TemplateColumn(TEMPLATE_EDITPHOT, orderable=False)
    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)

    class Meta:
        model=Photometry
        exclude=('sn', 'id')
