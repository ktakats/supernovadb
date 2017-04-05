from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

@python_2_unicode_compatible
class SN(models.Model):
    def __str__(self):
        return self.get_absolute_url()

    sn_name=models.CharField(max_length=100, unique=True)
    ra=models.FloatField(default=0.0)
    dec=models.FloatField(default=0.0)
    pi=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pi")
    coinvestigators=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="coinvestigator")

    def get_absolute_url(self):
        return reverse('view_sn', args=[self.id])

#@python_2_unicode_compatible
