from __future__ import unicode_literals

from django.db import models
from SNe.models import SN

# Create your models here.
class Obs(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='observations')
    obs_date=models.DateTimeField()
    obs_type=models.CharField(max_length=1, choices=(('S', 'Spectroscopy'), ('P', 'Photometry'), ('O', 'Other')), blank=True, null=True)
    telescope=models.CharField(max_length=100, blank=True, null=True)
    instrument=models.CharField(max_length=100, blank=True, null=True)
    setup=models.CharField(max_length=100, blank=True, null=True)
    notes=models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural="Observations"
