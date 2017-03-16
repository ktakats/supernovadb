from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.photometry, name='photometry'),
    url(r'^edit/(\d+)/$', views.photometry, name='editPhot'),
    url(r'^delete/(\d+)/$', views.deletePhot, name='deletePhot'),
    url(r'^query/$', views.queryPhot, name='queryPhot'),
]
