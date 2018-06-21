from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^raport$', views.raport, name='raport'),
    url(r'^raportAll$', views.raportAll, name='raportAll'),
    url(r'^dodanie_transakcji$', views.dodanie_transakcji,name='dodanie_transakcji'),
    url(r'^dodanie_konta$', views.dodanie_konta, name='dodanie_konta'),
    url(r'^dodanie_zlecenia_stalego$', views.dodanie_zlecenia_stalego, name='dodanie_zlecenia_stalego'),
    path('konto/<int:id>',views.konto_details, name='konto_details') 
]
