# Generated by Django 3.2.9 on 2021-11-20 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20211110_1335'),
        ('events', '0007_alter_eventinviterequest_to_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinEventRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_profile', to='account.profile')),
                ('to_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_event', to='events.event')),
            ],
        ),
    ]
