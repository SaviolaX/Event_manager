# Generated by Django 3.2.9 on 2021-11-14 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20211114_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventinviterequest',
            name='from_creator',
        ),
        migrations.RemoveField(
            model_name='eventinviterequest',
            name='to_event',
        ),
        migrations.AddField(
            model_name='eventinviterequest',
            name='from_event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_event', to='events.event'),
        ),
        migrations.AddField(
            model_name='eventinviterequest',
            name='to_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_profile', to='events.event'),
        ),
    ]