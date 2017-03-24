from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.spectroscopy, name='spectroscopy'),
    url(r'^delete/(\d+)/$', views.delSpectrum, name='delSpectrum'),
]
