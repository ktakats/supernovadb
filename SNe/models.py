from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class SN(models.Model):
    def __str__(self):
        return self.sn_name

    sn_name=models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('view_sn', args=[self.id])
