from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^add_sn/$', views.add_sn, name='add_sn'),
    url(r'^sn/(\d+)/$', views.view_sn, name='view_sn'),
    url(r'^sn/(\d+)/edit/$', views.edit_sn, name='edit_sn'),
    url(r'^sn/(\d+)/archive/$', views.archive_sn, name='archive_sn'),
    url(r'^my_stuff/$', views.my_stuff, name='my_stuff'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^projects/(\d+)/$', views.view_project, name="view_project"),
    url(r'^projects/(\d+)/edit/$', views.edit_project, name="edit_project"),
    url(r'^projects/(\d+)/archive/$', views.archive_project, name="archive_project"),
]
