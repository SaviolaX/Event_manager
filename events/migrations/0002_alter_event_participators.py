# Generated by Django 3.2.9 on 2021-11-12 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20211110_1335'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participators',
            field=models.ManyToManyField(blank=True, to='account.Profile'),
        ),
    ]