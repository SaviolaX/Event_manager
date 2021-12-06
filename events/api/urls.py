from django.urls import path

from .views import (EventList, CreateEvent, UpdateEvent,
                    EventView, JoinRequest, EventParticipators,
                    JoinEventRequestView, CancelJoinEvenRequest,
                    AcceptJoinEventRequest, DeclineJoinEventRequest,
                    KickEventParticipator, EventInvitationToUser,
                    CancelEventInvitationToUser, LeaveEvent)


app_name = 'api_events'


urlpatterns = [
    # Event profile
    path('all_events/', EventList.as_view(), name='all_events'),
    path('event/<int:id>/', EventView.as_view(), name='event_view'),
    path('create_event/', CreateEvent.as_view(), name='create_event'),
    path('event/<int:id>/edit/', UpdateEvent.as_view(), name='edit_event'),
    path('event/<int:id>/participators/', EventParticipators.as_view(),
         name='event_participators'),

    path('event/<int:event_id>/kick_participator/<int:profile_id>/',
         KickEventParticipator.as_view(), name='remove_participator'),
    path('event/<int:id>/leave_event/', LeaveEvent.as_view(),
         name='leave_event'),


    # Join event requests from user
    path('event/<int:event_id>/create_join_event_request/',
         JoinEventRequestView.as_view(), name='join_event_request'),
    path('event/<int:id>/cancel_join_event_request/',
         CancelJoinEvenRequest.as_view(), name='cancel_event_request'),

    path('event/<int:event_id>/accept_join_event/<int:req_id>/',
         AcceptJoinEventRequest.as_view(), name='accept_join_event'),
    path('event/<int:event_id>/decline_join_event/<int:req_id>/',
         DeclineJoinEventRequest.as_view(), name='decline_join_event'),

    # Join event requests list
    path('event/<int:id>/join_event_requests/', JoinRequest.as_view(),
         name='join_event_requests_list'),


    # Event invitation requests to user
    path('event/<int:event_id>/invite_user/<int:profile_id>/',
         EventInvitationToUser.as_view(), name='event_invite_request'),
    path('event/<int:event_id>/cancel_invite_to_user/<int:profile_id>/',
         CancelEventInvitationToUser.as_view(),
         name='cancel_event_invite_request'),
]
