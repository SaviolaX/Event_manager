from django.urls import path

from .views import (RegisterView, ProfileList, ProfileView,
                    ProfileFriends, FriendRequestList, EventInvitations,
                    ProfileEventsList, DeleteFriend, CreateFriendRequestView,
                    AcceptFriendRequest, DeclineFriendRequest,
                    CancelFriendRequest, AcceptEventInviteRequest,
                    DeclineEventInviteRequest)


app_name = 'api_account'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),

    # Profile
    path('all_profiles/', ProfileList.as_view(), name='all_profiles'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:id>/my_events/', ProfileEventsList.as_view(),
         name='my_events'),

    # Profile events invitations
    path('profile/<int:id>/invite_to_event_requests/',
         EventInvitations.as_view(), name='event_invites'),

    path('profile/<int:profile_id>/invite_to_event_requests/<int:req_id>/accept/',
         AcceptEventInviteRequest.as_view(), name='accept_event_intive'),
    path('profile/<int:profile_id>/invite_to_event_requests/<int:req_id>/decline/',
         DeclineEventInviteRequest.as_view(), name='decline_event_intive'),


    # Profile friends list
    path('profile/<int:id>/friends/', ProfileFriends.as_view(),
         name='friends'),
    path('profile/<int:profile_id>/delete_friend/<int:friend_id>/',
         DeleteFriend.as_view(), name='delete_friend'),

    # Profile requests
    path('profile/<int:id>/create_friend_request/',
         CreateFriendRequestView.as_view(), name='create_firend_request'),
    path('profile/<int:id>/friend_requests/', FriendRequestList.as_view(),
         name='friend_requests'),
    path('profile/<int:profile_id>/friend_requests/<int:req_id>/accept/',
         AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('profile/<int:profile_id>/friend_requests/<int:req_id>/cancel/',
         DeclineFriendRequest.as_view(), name='decline_friend_request'),
    path('profile/<int:id>/cancel_friend_request/',
         CancelFriendRequest.as_view(), name='cancel_friend_request'),

]
