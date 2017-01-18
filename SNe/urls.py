from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^add_sn/$', views.add_sn, name='add_sn'),
    url(r'^(\d+)/$', views.view_sn, name='view_sn'),
]
