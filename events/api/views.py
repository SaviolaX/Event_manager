from rest_framework import generics, status
from rest_framework.response import Response


from ..models import Event, JoinEventRequest
from accounts.models import Profile
from .serializers import (EventSerializer,
                          JoinEventRequestSerializer,
                          EventParticipatorsSerializer)


class EventList(generics.ListAPIView):
    """Get list of all events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventView(generics.RetrieveDestroyAPIView):
    """Get event detail or delete event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        """get event"""
        event = Event.objects.get(id=id)
        serializer = self.serializer_class(event)
        return Response(serializer.data)

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
    lookup_field = 'id'


class CreateEvent(generics.CreateAPIView):
    """Create event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UpdateEvent(generics.RetrieveUpdateAPIView):
    """Edit event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'


class JoinRequest(generics.ListAPIView):
    """Get a list of all event join requests"""
    queryset = JoinEventRequest.objects.all()
    serializer_class = JoinEventRequestSerializer
    lookup_field = 'id'
