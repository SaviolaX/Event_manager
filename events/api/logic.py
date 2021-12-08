from rest_framework import status
from rest_framework.response import Response

from ..models import Event, JoinEventRequest, EventInviteRequest
from accounts.models import Profile
from .serializers import EventSerializer


def leave_event(request, id):
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    if profile in event.participators.all():
        event.participators.remove(profile)
        return Response('You left event successfully',
                        status=status.HTTP_200_OK)
    else:
        return Response('You are not participator',
                        status=status.HTTP_403_FORBIDDEN)


def cancel_event_invite_request(request, event_id, profile_id):
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=event_id)
    if request.user == event.creator.user:
        event_invite = EventInviteRequest.objects.get(
            from_event=event, to_profile=profile)
        event_invite.delete()
        return Response('Invitation was canceled successfully',
                        status=status.HTTP_201_CREATED)
    else:
        return Response('Only event creator can cancel invites',
                        status=status.HTTP_403_FORBIDDEN)


def create_event_intite_to_user(request, event_id, profile_id):
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=event_id)
    if request.user == event.creator.user:
        event_invite, created = EventInviteRequest.objects.get_or_create(
            from_event=event, to_profile=profile)
        return Response('Invitation was sent successfully',
                        status=status.HTTP_201_CREATED)
    else:
        return Response('Only event creator can send invites',
                        status=status.HTTP_403_FORBIDDEN)


def kick_event_participator(request, event_id, profile_id):
    profile = Profile.objects.get(id=profile_id)
    event = Event.objects.get(id=event_id)
    if request.user.profile == event.creator:
        event.participators.remove(profile)
        return Response('User was removed from event participators',
                        status=status.HTTP_200_OK)
    else:
        return Response('Forbidden, you are not creator',
                        status=status.HTTP_403_FORBIDDEN)


def accept_join_event_request(request, event_id, req_id):
    event = Event.objects.get(id=event_id)
    join_event_request = JoinEventRequest.objects.get(id=req_id)
    if join_event_request.to_event.creator == request.user.profile:
        join_event_request.to_event.participators.add(
            join_event_request.from_profile)
        join_event_request.delete()
        return Response('User added to event participators',
                        status=status.HTTP_200_OK)
    else:
        return Response('You can not do it, you are not event creator',
                        status=status.HTTP_403_FORBIDDEN)


def decline_join_event_request(request, event_id, req_id):
    event = Event.objects.get(id=event_id)
    join_event_request = JoinEventRequest.objects.get(id=req_id)
    if join_event_request.to_event.creator == request.user.profile:
        join_event_request.delete()
        return Response('User added to event participators',
                        status=status.HTTP_200_OK)
    else:
        return Response('You can not do it, you are not event creator',
                        status=status.HTTP_403_FORBIDDEN)


def create_join_event_request(request, event_id):
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=event_id)
    if profile in event.participators.all():
        return Response("You are participator already",
                        status=status.HTTP_403_FORBIDDEN)
    else:
        join_event_request, created = JoinEventRequest.objects.get_or_create(
            from_profile=profile, to_event=event)
        return Response('Join event request was sent',
                        status=status.HTTP_200_OK)


def cancel_join_event_request(request, id):
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    join_event_request = JoinEventRequest.objects.get(
        from_profile=profile, to_event=event)
    if join_event_request:
        join_event_request.delete()
        return Response('Your request was canceled',
                        status=status.HTTP_200_OK)
    else:
        return Response('Join event request does not exist',
                        status=status.HTTP_400_BAD_REQUEST)


def delete_event(request, id):
    profile = Profile.objects.get(user=request.user)
    event = Event.objects.get(id=id)
    if event.creator == profile:
        event.delete()
    else:
        return Response('You are not creator and can not delete the event',
                        status=status.HTTP_403_FORBIDDEN)
    return Response('Event was deleted successfully',
                    status=status.HTTP_200_OK)


def get_event_page(request, id):
    event = Event.objects.get(id=id)
    serializer = EventSerializer(event)
    return Response(serializer.data)
