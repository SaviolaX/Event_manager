from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path('', views.all_events, name='all_events'),
    path('event/<int:id>/', views.event_page, name='event_page'),
    path('create_event/', views.create_event, name='create_event'),
    path('delete_event/<int:id>/', views.delete_event, name='delete_event'),
    path('edit_event/<int:id>/', views.edit_event, name='edit_event'),
    path('event/<int:id>/kick_participator/<str:profile_id>/',
         views.kick_event_participators, name='kick'),

    path('accept_event_request/<int:id>/',
         views.accept_event_invite, name='accept_event'),
    path('decline_event_request/<int:id>/',
         views.decline_event_invite, name='decline_event'),

    path('join_event/<int:id>/', views.join_event, name='join_event'),
    path('leave_event/<int:id>/', views.leave_event, name='leave_event'),

    path('event/<str:event_id>/people_to_invite/',
         views.profiles_list_for_inviting_to_event, name='invite_people'),
    path('event/<str:event_id>/invite_to_event/<str:profile_id>/',
         views.from_event_to_user_invite_request, name='invite_user_to_event'),
    path('event/<str:event_id>/people_to_invite/<str:profile_id>/',
         views.cancels_invite_request_to_user, name='cancel_event_invite'),
    path('event/<str:event_id>/friends_to_invite/',
         views.friends_list_for_inviting_to_event, name='invite_friends'),

    path('request_to_join_event/<str:event_id>/', views.request_join_event,
         name='join_event_request'),
    path('accept_join_event/<int:id>/', views.accept_join_event_request,
         name='accept_join_event_request'),
    path('decline_join_event/<int:id>/', views.decline_join_event_request,
         name='decline_join_event_request'),
    path('cancel_join_event_request/<int:id>/', views.cancel_join_request,
         name='cancel_join_event_request'),
]
