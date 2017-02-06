from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^add_sn/$', views.add_sn, name='add_sn'),
    url(r'^sn/(\d+)/$', views.view_sn, name='view_sn'),
    url(r'^sn/(\d+)/obslog/$', views.view_obslog, name='sn_obs'),
]
