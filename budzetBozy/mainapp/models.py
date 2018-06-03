from django.db import models
from datetime import date


class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=64)
    first_name = models.CharField("imię", max_length=15)
    last_name = models.CharField("nazwisko", max_length=20)

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField("saldo", max_digits=100, decimal_places=2)


class Currency(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    rate = models.DecimalField("kurs", max_digits=5, decimal_places=4)


class Category(models.Model):
    name = models.CharField("nazwa", max_length=100)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField("data", default=date.today)
    amount = models.DecimalField("kwota", max_digits=100, decimal_places=2)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name="waluta")
    categories = models.ManyToManyField(
        Category, verbose_name="kategoria")

    class Meta:
        ordering = ['-date']


class Permission(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view = models.BooleanField("przeglądanie", default=True)
    deposit = models.BooleanField("wpłacanie", default=True)
    withdraw = models.BooleanField("wypłacanie", default=False)
