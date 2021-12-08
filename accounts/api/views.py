from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from .logic import (get_profile_page, edit_profile_page, register_user,
                    get_profile_event_list, delete_friend,
                    create_friend_request, accept_friend_request,
                    decline_friend_request, cancel_friend_request,
                    get_all_profile_friends, accept_event_invite_request,
                    decline_event_invite_request)
from ..models import Profile, FriendRequest
from events.models import EventInviteRequest, Event
from events.api.serializers import EventSerializer
from .serializers import (RegisterSerializer, ProfileSerializer,
                          FriendRequestsSerializer, ProfileFriendsSerializer,
                          EventInviteRequestSerializer)


class DeclineEventInviteRequest(APIView):
    """User decline a request and request is deleted"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id, req_id):
        return decline_event_invite_request(request, profile_id, req_id)


class AcceptEventInviteRequest(APIView):
    """User accept a request and event add him to participators list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id, req_id):
        return accept_event_invite_request(request, profile_id, req_id)


class ProfileFriends(generics.ListAPIView):
    """Get profile friend's list"""
    queryset = Profile.objects.all()
    serializer_class = ProfileFriendsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        return get_all_profile_friends(request, id)


class FriendRequestList(generics.ListAPIView):
    """Get a list of all friend requests to the user"""
    serializer_class = FriendRequestsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return FriendRequest.objects.filter(to_user=profile)


class CancelFriendRequest(APIView):
    """Cancel sent friend request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        return cancel_friend_request(request, id)


class DeclineFriendRequest(APIView):
    """Decline request from another user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, req_id, profile_id):
        return decline_friend_request(request, req_id, profile_id)


class AcceptFriendRequest(APIView):
    """Accept request from another user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, req_id, profile_id):
        return accept_friend_request(request, req_id, profile_id)


class CreateFriendRequestView(APIView):
    """Create a friend request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        return create_friend_request(request, id)


class DeleteFriend(APIView):
    """Delete friend from profile's friend list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id, friend_id, format=None):
        return delete_friend(request, profile_id, friend_id)


class ProfileEventsList(generics.RetrieveAPIView):
    """Get events list created by profile"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        return get_profile_event_list(request, id)


class EventInvitations(generics.ListAPIView):
    """Get a list of event requests to current user"""
    serializer_class = EventInviteRequestSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return EventInviteRequest.objects.filter(to_profile=profile)


class ProfileList(generics.ListAPIView):
    """Get a list of all existing profiles"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get a profile view(detail) or update (only current user) profile"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        """Get profile page"""
        return get_profile_page(request, id)

    def update(self, request, id=None):
        """If profile belong to current user, profile can be edited"""
        return edit_profile_page(request, id)


class RegisterView(generics.GenericAPIView):
    """Create user account and profile for a new user"""
    serializer_class = RegisterSerializer

    def post(self, request):
        """Create user"""
        return register_user(request)
