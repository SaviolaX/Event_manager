from django.shortcuts import render

from .models import Event, JoinEventRequest
from account.models import Profile
from account.account_logic import *


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
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    join_event_requests = JoinEventRequest.objects.all().filter(to_event=event)
    join_event_request = JoinEventRequest.objects.filter(
        from_profile=profile).first()

    context = {'event': event, 'join_event_requests': join_event_requests,
               'join_event_request': join_event_request, 'profile': profile}
    return render(request, 'events/event_page.html', context)


def get_list_of_all_users(request, event_id):
    """Get list of all users"""
    event = Event.objects.get(id=event_id)
    profiles = Profile.objects.all()
    requests = EventInviteRequest.objects.filter(from_event=event)

    context = {'profiles': profiles, 'event': event, 'requests': requests}
    return render(request, 'events/invite_all_profiles_to_event.html', context)


def get_list_of_all_friends(request, event_id):
    """Get list of all friends"""
    event = Event.objects.get(id=event_id)
    friends = get_profile_all_friends(request)

    context = {'friends': friends, 'event': event}
    return render(request, 'events/invite_friends.html', context)
