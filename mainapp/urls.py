from django.conf.urls import url
from django.urls import path


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^raport$', views.raport, name='raport'),
    url(r'^raportAll$', views.raportAll, name='raportAll'),
    url(r'^dodanie_transakcji$', views.dodanie_transakcji,name='dodanie_transakcji'),
    path('usuwanie_transakcji/<int:id>', views.usuwanie_transakcji,name='usuwanie_transakcji'),
    url(r'^dodanie_kategorii$', views.dodanie_kategorii, name='dodanie_kategorii'),
    path('usuwanie_kategorii/<int:id>',views.usuwanie_kategorii, name='usuwanie_kategorii'),
    url(r'^dodanie_konta$', views.dodanie_konta, name='dodanie_konta'),
    path('usuwanie_konta/<int:id>', views.usuwanie_konta,name='usuwanie_konta'),
    url(r'^dodanie_zlecenia_stalego$', views.dodanie_zlecenia_stalego, name='dodanie_zlecenia_stalego'),
    path('konto/<int:id>',views.konto_details, name='konto_details'),
    path('raport_pdf',views.raport_pdf, name='raport_pdf'),
]
