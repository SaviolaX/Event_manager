from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

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
        profile = Profile.objects.get(id=profile_id)
        e_request = EventInviteRequest.objects.get(id=req_id)
        if e_request.to_profile == request.user.profile:
            e_request.delete()
            return Response('Event invitation was canceled successfully',
                            status=status.HTTP_200_OK)
        else:
            return Response('You can not cancel invitation, it is not yours',
                            status=status.HTTP_403_FORBIDDEN)


class AcceptEventInviteRequest(APIView):
    """User accept a request and event add him to participators list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id, req_id):
        profile = Profile.objects.get(id=profile_id)
        e_request = EventInviteRequest.objects.get(id=req_id)
        if e_request.to_profile == request.user.profile:
            e_request.from_event.participators.add(e_request.to_profile)
            e_request.delete()
            return Response('Event invitation was accepted successfully',
                            status=status.HTTP_200_OK)
        else:
            return Response(
                'Invitation was sent not for you, you can not accept it',
                status=status.HTTP_403_FORBIDDEN)


class ProfileFriends(generics.ListAPIView):
    """Get profile friend's list"""
    queryset = Profile.objects.all()
    serializer_class = ProfileFriendsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        profile = Profile.objects.get(id=id)
        friends = profile.friends.all()
        serializer = ProfileSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        profile = Profile.objects.get(id=id)
        sent_requests = FriendRequest.objects.filter(
            from_user=request.user.profile, to_user=profile).first()
        if sent_requests.from_user == request.user.profile:
            sent_requests.delete()
            return Response('Your friend request was canceled',
                            status=status.HTTP_200_OK)
        else:
            return Response('You can not cancel not your request',
                            status=status.HTTP_403_FORBIDDEN)


class DeclineFriendRequest(APIView):
    """Decline request from another user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, req_id, profile_id):
        profile = Profile.objects.get(id=profile_id)
        f_request = FriendRequest.objects.get(id=req_id)
        if f_request.to_user == request.user.profile:
            f_request.delete()
            return Response('Friend request canceled',
                            status=status.HTTP_200_OK)
        elif f_request.from_user == request.user.profile:
            f_request.delete()
            return Response('Friend request canceled',
                            status=status.HTTP_200_OK)
        else:
            return Response('You can not decline not your request',
                            status=status.HTTP_403_FORBIDDEN)


class AcceptFriendRequest(APIView):
    """Accept request from another user"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, req_id, profile_id):
        profile = Profile.objects.get(id=profile_id)
        f_request = FriendRequest.objects.get(id=req_id)
        if f_request.to_user == request.user.profile:
            f_request.to_user.friends.add(f_request.from_user)
            f_request.from_user.friends.add(f_request.to_user)
            f_request.delete()
            return Response('Friend request accepted',
                            status=status.HTTP_200_OK)
        else:
            return Response('You can not accept not your request',
                            status=status.HTTP_403_FORBIDDEN)


class CreateFriendRequestView(APIView):
    """Create a friend request"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            to_user = get_object_or_404(Profile, id=id)
            profile = Profile.objects.get(user=request.user)
            f_request, created = FriendRequest.objects.get_or_create(
                from_user=profile,
                to_user=to_user)
            return Response({'create friend request': True})
        except FriendRequest.DoesNotExist:
            return Response({'Something happened with function': True})


class DeleteFriend(APIView):
    """Delete friend from profile's friend list"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id, friend_id, format=None):
        profile = Profile.objects.get(id=profile_id)
        friend = profile.friends.get(id=friend_id)
        profile.friends.remove(friend)
        friend.friends.remove(profile)
        return Response({'delete friend': True})


class ProfileEventsList(generics.RetrieveAPIView):
    """Get events list created by profile"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, id=None):
        profile = Profile.objects.get(id=id)
        events = Event.objects.all().filter(creator=profile)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        try:
            profile = Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response('Profile does not exist, wrong address',
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, id=None):
        """If profile belong to current user, profile can be edited"""
        profile = Profile.objects.get(id=id)
        if request.user.profile == profile:
            serializer = ProfileSerializer(instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response('Something went wrong',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('You cant not edit profile',
                            status=status.HTTP_403_FORBIDDEN)


class RegisterView(generics.GenericAPIView):
    """Create user account and profile for a new user"""
    serializer_class = RegisterSerializer

    def post(self, request):
        """Create user"""
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
