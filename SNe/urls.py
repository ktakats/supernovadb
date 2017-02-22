from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^add_sn/$', views.add_sn, name='add_sn'),
    url(r'^sn/(\d+)/$', views.view_sn, name='view_sn'),
    url(r'^sn/(\d+)/obslog/$', views.view_obslog, name='sn_obs'),
    url(r'^sn/(\d+)/obslog/delete/(\d+)/$', views.deleteobs, name='deleteObs'),
    url(r'^sn/(\d+)/obslog/edit/(\d+)/$', views.view_obslog, name='editObs'),
    url(r'^sn/(\d+)/photometry/$', views.photometry, name='photometry'),
    url(r'^sn/(\d+)/photometry/edit/(\d+)/$', views.photometry, name='editPhot'),
    url(r'^sn/(\d+)/photometry/delete/(\d+)/$', views.deletePhot, name='deletePhot'),
]
