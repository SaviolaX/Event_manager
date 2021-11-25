from django.shortcuts import redirect

from .models import Event, JoinEventRequest
from account.models import Profile


def instantly_join_event_without_requests(request, id):
    """Add current user profile to an event participators"""
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    event.participators.add(profile)
    return redirect('events:event_page', event.id)


def user_sends_create_request_to_join_event(request, event_id):
    """Create joint request between profile and event"""
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=event_id)
    join_event_request, created = JoinEventRequest.objects.get_or_create(
        from_profile=profile, to_event=event)
    return redirect('events:event_page', event.id)


def cancel_and_delete_join_request(request, id):
    """Gets sent join event request and delete it"""
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    join_event_request = JoinEventRequest.objects.get(
        from_profile=profile, to_event=event)
    join_event_request.delete()
    return redirect('events:event_page', event.id)


def add_user_to_event_participators(request, id):
    """Accept join request and add user to event participators"""
    join_event_request = JoinEventRequest.objects.get(id=id)
    if join_event_request.to_event.creator == request.user.profile:
        join_event_request.to_event.participators.add(
            join_event_request.from_profile)
        join_event_request.delete()
        return redirect('events:event_page', join_event_request.to_event.id)


def decline_to_join_then_delete_request(request, id):
    """Decline join request and delete join request"""
    join_event_request = JoinEventRequest.objects.get(id=id)
    if join_event_request.to_event.creator == request.user.profile:
        join_event_request.delete()
        return redirect('events:event_page', join_event_request.to_event.id)
