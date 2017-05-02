from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from Comments.models import Comment


@python_2_unicode_compatible
class SN(models.Model):
    def __str__(self):
        return self.sn_name

    sn_name=models.CharField(max_length=100, unique=True)
    ra=models.FloatField(default=0.0)
    dec=models.FloatField(default=0.0)
    pi=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pi")
    coinvestigators=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="coinvestigator")
    sntype=models.CharField(max_length=5, blank=True, null=True)
    host=models.CharField(max_length=20, blank=True, null=True)
    z=models.FloatField(blank=True, null=True)
    comments=models.ManyToManyField(Comment, related_name="sn_comment")

    class Meta:
        verbose_name_plural="SNe"

    def get_absolute_url(self):
        return reverse('view_sn', args=[self.id])

@python_2_unicode_compatible
class Project(models.Model):

    title=models.CharField(max_length=100, blank=False)
    description=models.CharField(max_length=500)
    pi=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_pi", null=True)
    coinvestigators=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="project_coi")
    sne=models.ManyToManyField(SN, related_name="project_sne")
    comments=models.ManyToManyField(Comment, related_name="project_comment")

    def get_absolute_url(self):
        return reverse('view_project', args=[self.id])

    def __str__(self):
        return self.title
