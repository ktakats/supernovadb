from __future__ import unicode_literals

from django.db import models
from django_mysql.models import ListTextField


from SNe.models import SN


# Create your models here.

class Spectrum(models.Model):
    sn = models.ForeignKey(SN, on_delete=models.CASCADE, related_name='spectroscopy')
    MJD = models.FloatField()
    notes = models.CharField(max_length=200, blank=True, null=True)
    wavelength=ListTextField(base_field=models.IntegerField(), blank=True)
    flux=ListTextField(base_field=models.IntegerField(), blank=True)

    def as_dict(self):
        return {
            "MJD": self.MJD,
        }

    def __str__(self):
        return self.sn+str(self.MJD)

    class Meta:
        verbose_name_plural = "Spectra"

