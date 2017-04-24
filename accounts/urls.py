from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^logout/', views.logout_view, name="logout"),
]
