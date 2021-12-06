from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from ..models import Event, JoinEventRequest, EventInviteRequest
from accounts.models import Profile
from .serializers import (EventSerializer,
                          JoinEventRequestSerializer,
                          EventParticipatorsSerializer)


class LeaveEvent(APIView):
    """Remove profile from participators list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        profile = Profile.objects.get(user=request.user)
        event = Event.objects.get(id=id)
        if profile in event.participators.all():
            event.participators.remove(profile)
            return Response('You left event successfully',
                            status=status.HTTP_200_OK)
        else:
            return Response('You are not participator',
                            status=status.HTTP_403_FORBIDDEN)


class CancelEventInvitationToUser(APIView):
    """Event sends an invite to user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
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


class EventInvitationToUser(APIView):
    """Event sends an invite to user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
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


class KickEventParticipator(APIView):
    """Remove participator from event"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
        profile = Profile.objects.get(id=profile_id)
        event = Event.objects.get(id=event_id)
        if request.user.profile == event.creator:
            event.participators.remove(profile)
            return Response('User was removed from event participators',
                            status=status.HTTP_200_OK)
        else:
            return Response('Forbidden, you are not creator',
                            status=status.HTTP_403_FORBIDDEN)


class AcceptJoinEventRequest(APIView):
    """Accept join event request from user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, req_id):
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


class DeclineJoinEventRequest(APIView):
    """Decline join event request from user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, req_id):
        event = Event.objects.get(id=event_id)
        join_event_request = JoinEventRequest.objects.get(id=req_id)
        if join_event_request.to_event.creator == request.user.profile:
            join_event_request.delete()
            return Response('User added to event participators',
                            status=status.HTTP_200_OK)
        else:
            return Response('You can not do it, you are not event creator',
                            status=status.HTTP_403_FORBIDDEN)


class JoinEventRequestView(APIView):
    """Create join event request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
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


class CancelJoinEvenRequest(APIView):
    """Cancel join event request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
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


class EventList(generics.ListAPIView):
    """Get list of all events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class EventView(generics.RetrieveDestroyAPIView):
    """Get event detail or delete event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        """get event"""
        try:
            event = Event.objects.get(id=id)
            serializer = self.serializer_class(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response('Wrong event, probably event does not exist')

    def delete(self, request, id=None):
        """delete event"""
        profile = Profile.objects.get(user=self.request.user)
        event = Event.objects.get(id=id)
        if event.creator == profile:
            event.delete()
        else:
            return Response('You are not creator and can not delete the event',
                            status=status.HTTP_403_FORBIDDEN)
        return Response('Event was deleted successfully',
                        status=status.HTTP_200_OK)


class EventParticipators(generics.ListAPIView):
    """Get a list of event participators"""
    queryset = Event.objects.all()
    serializer_class = EventParticipatorsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class CreateEvent(generics.CreateAPIView):
    """Create event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class UpdateEvent(generics.RetrieveUpdateAPIView):
    """Edit event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class JoinRequest(generics.ListAPIView):
    """Get a list of all event join requests"""
    queryset = JoinEventRequest.objects.all()
    serializer_class = JoinEventRequestSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
