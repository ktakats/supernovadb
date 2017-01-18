from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
@python_2_unicode_compatible
class SN(models.Model):
    def __str__(self):
        return self.sn_name

    sn_name=models.CharField(max_length=100)
