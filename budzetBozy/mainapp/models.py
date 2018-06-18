from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="użytkownik")
    name = models.CharField("nazwa", max_lenth=15)
    balance = models.DecimalField("saldo", max_digits=100, decimal_places=2)

    class Meta:
        verbose_name = "konto"
        verbose_name_plural = "konta"


class Currency(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    rate = models.DecimalField("kurs", max_digits=5, decimal_places=4)

    class Meta:
        verbose_name = "waluta"
        verbose_name_plural = "waluty"


class Category(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField("nazwa", max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "kategoria"
        verbose_name_plural = "kategorie"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField("tytuł",max_length=50, default='')
    date = models.DateField("data", default=date.today)
    amount = models.DecimalField("kwota", max_digits=100, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="waluta")
    categories = models.ManyToManyField(Category, verbose_name="kategoria")

    class Meta:
        ordering = ['-date']
        verbose_name = "transakcja"
        verbose_name_plural = "transakcje"


class Permission(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.BooleanField("właściciel", default=True)

    class Meta:
        verbose_name = "uprawnienia"

class StandingOrder(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    account = models.ForeignKey(Account, on_delete=models.CASCADE) 
    title = models.CharField("tytuł", max_length=30, default='') 
    amount = models.DecimalField("kwota", max_digits=100, decimal_places=2) 
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="waluta") 
    categories = models.ManyToManyField(Category, verbose_name="kategoria") 
    next_date = models.DateField("data następnego wykonania", default=date.today) 
    frequency = models.IntegerField("częstotliwość") 
 
    class Meta: 
        ordering = ['next_date']
        verbose_name = "zlecenie stałe"
        verbose_name_plural = "zlecenia stałe" 