# Generated by Django 3.2.7 on 2021-11-30 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='event title')),
                ('description', models.TextField(blank=True, verbose_name='event description')),
                ('start', models.CharField(max_length=5, verbose_name='time event starts')),
                ('finish', models.CharField(max_length=5, verbose_name='time event finish')),
                ('event_date', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('privat_event', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='accounts.profile', verbose_name='event creator')),
                ('participators', models.ManyToManyField(blank=True, to='accounts.Profile', verbose_name='event participators')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='JoinEventRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_profile', to='accounts.profile')),
                ('to_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_event', to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventInviteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_event', to='events.event')),
                ('to_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_profile', to='accounts.profile')),
            ],
        ),
    ]
