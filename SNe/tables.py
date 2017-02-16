import django_tables2 as tables
from .models import Obs

class ObsLogTable(tables.Table):
    obs_date=tables.DateColumn(short=True, verbose_name='Date')
    obs_type=tables.Column(verbose_name="Type")

    class Meta:
        model=Obs
        exclude=('sn')
