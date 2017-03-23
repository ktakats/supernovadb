from __future__ import unicode_literals

from django.db import models
from SNe.models import SN

FILTERCHOICES=(('U', 'U'), ('B', 'B'), ('V', 'V'), ('R', 'R'), ('I', 'I'), ('J', 'J'), ('H', 'H'), ('K', 'K'), ('g', 'g'), ('r', 'r'), ('i', 'i'), ('z', 'z'))

# Create your models here.
class Photometry(models.Model):

    sn=models.ForeignKey(SN, on_delete=models.CASCADE, related_name='photometry')
    MJD=models.DecimalField(max_digits=7, decimal_places=2)
    Filter=models.CharField(max_length=2, choices=FILTERCHOICES)
    magnitude=models.FloatField()
    mag_error=models.FloatField()
    notes=models.CharField(max_length=200, blank=True)

    def as_dict(self):
        return {
            "MJD": self.MJD,
            "Filter": self.Filter,
            "magnitude": self.magnitude,
            "mag_error": self.mag_error,
        }
