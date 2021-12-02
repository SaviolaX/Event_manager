from rest_framework import serializers

from ..models import Event, JoinEventRequest


class EventParticipatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('participators',)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'title', 'event_date', 'start', 'finish',
                  'timestamp', 'creator', 'privat_event', 'participators')


class JoinEventRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinEventRequest
        fields = '__all__'
