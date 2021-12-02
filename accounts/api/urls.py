from django.urls import path

from .views import (RegisterView, ProfileList, ProfileView,
                    ProfileFriends, FriendRequestList, EventInvitations,
                    ProfileEventsList, DeleteFriend, CreateFriendRequestView)


app_name = 'api_account'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),

    path('all_profiles/', ProfileList.as_view(), name='all_profiles'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:id>/friends/', ProfileFriends.as_view(),
         name='friends'),
    path('profile/<int:id>/my_events/', ProfileEventsList.as_view(),
         name='my_events'),

    path('profile/<int:id>/create_friend_request/',
         CreateFriendRequestView.as_view()),

    path('profile/<int:profile_id>/delete_friend/<int:friend_id>/',
         DeleteFriend.as_view(), name='delete_friend'),

    path('profile/<int:id>/friend_requests/', FriendRequestList.as_view(),
         name='friend_requests'),
    path('profile/<int:id>/invite_to_event_requests/',
         EventInvitations.as_view(), name='event_invites'),
]
