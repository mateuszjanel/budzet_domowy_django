# Generated by Django 2.0.6 on 2018-06-21 08:47

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=100, verbose_name='saldo'),
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=25, verbose_name='nazwa'),
        ),
        migrations.RemoveField(
            model_name='standingorder',
            name='categories',
        ),
        migrations.AddField(
            model_name='standingorder',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Category', verbose_name='kategoria'),
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='categories',
        ),
        migrations.AddField(
            model_name='transaction',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.Category', verbose_name='kategoria'),
        ),
    ]