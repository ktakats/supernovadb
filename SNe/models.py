from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import date
from django.utils import timezone


@python_2_unicode_compatible
class SN(models.Model):
    def __str__(self):
        return self.sn_name

    sn_name=models.CharField(max_length=100, unique=True)
    ra=models.FloatField(default=0.0)
    dec=models.FloatField(default=0.0)

    def get_absolute_url(self):
        return reverse('view_sn', args=[self.id])

#@python_2_unicode_compatible
class Obs(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='observations')
    obs_date=models.DateTimeField()
    obs_type=models.CharField(max_length=1, choices=(('S', 'Spectroscopy'), ('P', 'Photometry'), ('O', 'Other')), blank=True)
    telescope=models.CharField(max_length=100)
    instrument=models.CharField(max_length=100, blank=True)
    setup=models.CharField(max_length=100, blank=True)
    notes=models.CharField(max_length=200, blank=True)

class Photometry(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='photometry')
    MJD=models.DecimalField(max_digits=7, decimal_places=2)
    Filter=models.CharField(max_length=15)
    magnitude=models.FloatField()
    mag_error=models.FloatField()
    notes=models.CharField(max_length=200, blank=True)
