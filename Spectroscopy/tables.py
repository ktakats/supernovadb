import django_tables2 as tables
from .models import Spectrum

TEMPLATE_EDITPHOT='<a href="#confirmmodal"  data-toggle="modal" data-id="{{record.pk}}" title="delete"><i class="fa fa-trash-o"></i></a>'

class SpectroscopyTable(tables.Table):
    options=tables.TemplateColumn(TEMPLATE_EDITPHOT, orderable=False)
    selection = tables.CheckBoxColumn(accessor="pk", attrs = { "th__input":
                                        {"onclick": "toggle(this)"}},
                                        orderable=False)

    class Meta:
        model=Spectrum
        exclude=('sn', 'spectrum')
