# Generated by Django 2.0.6 on 2018-06-10 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standingorder',
            name='title',
            field=models.CharField(default='', max_length=30, verbose_name='nazwa'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='title',
            field=models.CharField(default='', max_length=50),
        ),
    ]