from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index', views.index, name = 'index'),
    url(r'^authorization', views.authorization, name = 'authorization'),
    url(r'^data', views.login, name = 'data')
]