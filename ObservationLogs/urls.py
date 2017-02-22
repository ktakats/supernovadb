from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.view_obslog, name='sn_obs'),
    url(r'^delete/(\d+)/$', views.deleteobs, name='deleteObs'),
    url(r'^edit/(\d+)/$', views.view_obslog, name='editObs'),
]
