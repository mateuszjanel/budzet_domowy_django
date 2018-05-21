from django.db import models
from datetime import date

class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    first_name = models.CharField("imię",max_length=100)
    last_name = models.CharField("nazwisko",max_length=100)
    type = models.CharField(max_length=100)

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField("saldo",max_digits=100,decimal_places=2)
    
class Currency(models.Model):
    id = models.CharField(max_length=3,primary_key=True)
    rate = models.DecimalField("kurs",max_digits=5,decimal_places=4)

class Category(models.Model):
    name = models.CharField("nazwa",max_length=100)

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    date = models.DateField("data",default=date.today)
    amount = models.DecimalField("kwota",max_digits=100,decimal_places=2)
    currency = models.ForeignKey(Currency,on_delete = models.CASCADE,verbose_name="waluta")
    category = models.ForeignKey(Category,on_delete = models.CASCADE, verbose_name="kategoria")

class Accounts_privilages(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    view = models.BooleanField("przeglądanie")
    in = models.BooleanField("wpłacanie")
    out = models.BooleanField("wypłacanie")
