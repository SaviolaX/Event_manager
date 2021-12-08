from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from ..models import Event, JoinEventRequest
from .serializers import (EventSerializer,
                          JoinEventRequestSerializer,
                          EventParticipatorsSerializer)
from .logic import (get_event_page, delete_event, cancel_join_event_request,
                    create_join_event_request, decline_join_event_request,
                    accept_join_event_request, kick_event_participator,
                    create_event_intite_to_user, cancel_event_invite_request,
                    leave_event)


class LeaveEvent(APIView):
    """Remove profile from participators list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        return leave_event(request, id)


class CancelEventInvitationToUser(APIView):
    """Event sends an invite to user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
        return cancel_event_invite_request(request, event_id, profile_id)


class EventInvitationToUser(APIView):
    """Event sends an invite to user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
        return create_event_intite_to_user(request, event_id, profile_id)


class KickEventParticipator(APIView):
    """Remove participator from event"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, profile_id):
        return kick_event_participator(request, event_id, profile_id)


class AcceptJoinEventRequest(APIView):
    """Accept join event request from user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, req_id):
        return accept_join_event_request(request, event_id, req_id)


class DeclineJoinEventRequest(APIView):
    """Decline join event request from user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id, req_id):
        return decline_join_event_request(request, event_id, req_id)


class CreateJoinEventRequest(APIView):
    """Create join event request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        return create_join_event_request(request, event_id)


class CancelJoinEvenRequest(APIView):
    """Cancel join event request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        return cancel_join_event_request(request, id)


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
            return get_event_page(request, id)
        except Event.DoesNotExist:
            return Response('Wrong event, probably event does not exist')

    def delete(self, request, id=None):
        """delete event"""
        return delete_event(request, id)


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
