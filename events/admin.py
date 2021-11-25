from django.contrib import admin

from .models import Event, EventInviteRequest, JoinEventRequest


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'event_date',
                    'start', 'finish', 'privat_event']
    list_filter = ['title', 'creator', 'event_date', 'privat_event']


@admin.register(EventInviteRequest)
class EventInviteRequestAdmin(admin.ModelAdmin):
    list_display = ['from_event', 'to_profile', 'timestamp']
    list_filter = ['from_event', 'to_profile', 'timestamp']


@admin.register(JoinEventRequest)
class JoinEventRequestAdmin(admin.ModelAdmin):
    list_display = ['from_profile', 'to_event', 'timestamp']
    list_filter = ['from_profile', 'to_event', 'timestamp']
