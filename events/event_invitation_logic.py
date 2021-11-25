from django.shortcuts import redirect

from .models import Event, EventInviteRequest
from account.models import Profile
from account.account_logic import *


def kick_participator_from_event(request, id, profile_id):
    """
    Only for event creator
    Remove profile from list of participators
    """
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=id)
    event.participators.remove(profile)
    return redirect('events:event_page', event.id)


def event_sends_invite_request_to_user(request, event_id, profile_id):
    """Sends invite request from event to profile"""
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=event_id)
    event_invite, created = EventInviteRequest.objects.get_or_create(
        request, from_event=event, to_profile=profile)
    return redirect('events:event_page', event.id)


def event_cancels_invite_request_to_user(request, event_id, profile_id):
    """Cancels invite request from event to profile"""
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=event_id)
    invite_event_request = EventInviteRequest.objects.get(
        from_event=event, to_profile=profile)
    invite_event_request.delete()
    return redirect('events:invite_people', event.id)


def remove_user_from_event_participators(request, id):
    """Remove profile from participators list"""
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    if profile in event.participators.all():
        event.participators.remove(profile)
    return redirect('events:event_page', event.id)


def accept_invitation(request, id):
    """User accept a request and event add him to participators list"""
    e_request = EventInviteRequest.objects.get(id=id)
    if e_request.to_profile == request.user.profile:
        e_request.from_event.participators.add(e_request.to_profile)
        e_request.delete()
        return redirect('events:event_page', e_request.from_event.id)


def decline_invitation(request, id):
    """User decline a request and request is deleted"""
    e_request = get_event_invite_request(request, id=id)
    if e_request.to_profile == request.user.profile:
        e_request.delete()
        return redirect('account:profile', e_request.to_profile.id)
