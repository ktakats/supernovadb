from django.contrib import admin

# Register your models here.
from .models import SN, Project

admin.site.register(SN)
admin.site.register(Project)
