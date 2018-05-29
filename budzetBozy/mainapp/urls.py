from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^raport$', views.raport, name='raport'),
    url(r'^(?P<param2>[a-z]*)/(?P<param1>[a-z]*)$', views.podstrona, name='podstrona')
]
