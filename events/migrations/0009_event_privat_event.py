# Generated by Django 3.2.9 on 2021-11-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_joineventrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='privat_event',
            field=models.BooleanField(default=False),
        ),
    ]
