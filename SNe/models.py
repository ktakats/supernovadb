from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
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
