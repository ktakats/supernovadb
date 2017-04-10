from django.conf.urls import include, url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^add_sn/$', views.add_sn, name='add_sn'),
    url(r'^sn/(\d+)/$', views.view_sn, name='view_sn'),
    url(r'^my_sne/$', views.my_sne, name='my_sne'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^projects/(\d+)/$', views.view_project, name="view_project")
]
