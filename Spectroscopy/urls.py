from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.spectroscopy, name='spectroscopy'),
    url(r'^delete/$', views.delSpectrum, name='delSpectrum'),
    url(r'^query/$', views.query, name='query')
]
