# Generated by Django 3.2.9 on 2021-11-09 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='friends',
            field=models.ManyToManyField(default='', to='account.Profile'),
        ),
    ]
