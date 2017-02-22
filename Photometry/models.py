from __future__ import unicode_literals

from django.db import models
from SNe.models import SN

# Create your models here.
class Photometry(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='photometry')
    MJD=models.DecimalField(max_digits=7, decimal_places=2)
    Filter=models.CharField(max_length=15)
    magnitude=models.FloatField()
    mag_error=models.FloatField()
    notes=models.CharField(max_length=200, blank=True)
