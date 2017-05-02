from __future__ import unicode_literals

from django.db import models

from SNe.models import SN

# Create your models here.

class Spectrum(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='spectroscopy')
    MJD=models.FloatField()
    notes=models.CharField(max_length=200, blank=True)

    def as_dict(self):
        return {
            "MJD": self.MJD,
        }

    class Meta:
        verbose_name_plural="Spectra"


class SpectrumDataPoint(models.Model):

    spectrum=models.ForeignKey(Spectrum, on_delete=models.CASCADE, related_name="datapoint")
    wavelength=models.FloatField()
    flux=models.DecimalField(max_digits=15, decimal_places=5)

    def as_dict(self):
        return {
            "wavelength": self.wavelength,
            "flux": self.flux
        }
