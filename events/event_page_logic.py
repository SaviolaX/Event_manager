from django.shortcuts import render

from .models import Event, JoinEventRequest
from accounts.models import Profile
from accounts.account_logic import *


def get_event_by_id(request, id):
    """Get event by id from data base"""
    event = Event.objects.get(id=id)
    return event


def get_all_open_events(request):
    """Get all events whose "private" == False"""
    events = Event.objects.all().filter(privat_event=False)

    context = {'events': events}
    return render(request, 'events/events.html', context)


def get_event_page(request, id):
    """Get event page"""
    event = Event.objects.select_related('creator').prefetch_related(
        'participators').get(id=id)
    join_event_requests = JoinEventRequest.objects.select_related(
        'to_event', 'from_profile__user')

    context = {'event': event, 'join_event_requests': join_event_requests}
    return render(request, 'events/event_page.html', context)


def get_list_of_all_users(request, event_id):
    """Get list of all users"""
    event = Event.objects.get(id=event_id)
    profiles = Profile.objects.select_related('user').all()

    context = {'profiles': profiles, 'event': event}
    return render(request, 'events/invite_all_profiles_to_event.html', context)


def get_list_of_all_friends(request, event_id):
    """Get list of all friends"""
    event = Event.objects.get(id=event_id)
    friends = get_profile_all_friends(request)

    context = {'friends': friends, 'event': event}
    return render(request, 'events/invite_friends.html', context)
