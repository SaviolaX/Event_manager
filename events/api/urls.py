from django.urls import path

from .views import (EventList, CreateEvent, UpdateEvent,
                    EventView, JoinRequest, EventParticipators)


app_name = 'api_events'


urlpatterns = [
    path('all_events/', EventList.as_view(), name='all_events'),
    path('event/<int:id>/', EventView.as_view(), name='event_view'),
    path('create_event/', CreateEvent.as_view(), name='create_event'),
    path('edit_event/<int:id>/', UpdateEvent.as_view(), name='edit_event'),
    path('event/<int:id>/participators/', EventParticipators.as_view(),
         name='event_participators'),

    path('event/<int:id>/join_event_requests/', JoinRequest.as_view(),
         name='join_event_request'),
]
