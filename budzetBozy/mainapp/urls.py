from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^raport$', views.raport, name='raport'),
    url(r'^dodanie_transakcji$', views.dodanie_transakcji, name='dodanie_transakcji'),
    url(r'^dodanie_kategorii$', views.dodanie_kategorii, name='dodanie_kategorii'),
]
