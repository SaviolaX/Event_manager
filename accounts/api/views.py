from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Profile, FriendRequest
from events.models import EventInviteRequest, Event
from events.api.serializers import EventSerializer
from .serializers import (RegisterSerializer, ProfileSerializer,
                          FriendRequestsSerializer, ProfileFriendsSerializer,
                          EventInviteRequestSerializer)


class CreateFriendRequestView(APIView):  # Don't work
    def post(self, request, id=None):
        to_user = Profile.objects.get(id=id)
        FriendRequest.objects.create(
            from_user=request.user,
            to_user=to_user)
        return Response({'status': 'Request sent'}, status=201)


class DeleteFriend(APIView):  # Don't work
    def post(self, request, profile_id, friend_id, format=None):
        profile = Profile.objects.get(id=profile_id)
        friend = profile.friends.get(id=friend_id)
        profile.friends.remove(friend)
        friend.friends.remove(profile)
        return Response({'delete friend': True})


class ProfileEventsList(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        profile = Profile.objects.get(id=id)
        events = Event.objects.all().filter(creator=profile)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventInvitations(generics.ListAPIView):
    serializer_class = EventInviteRequestSerializer
    lookup_field = 'id'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return EventInviteRequest.objects.filter(to_profile=profile)


class FriendRequestList(generics.ListAPIView):
    serializer_class = FriendRequestsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return FriendRequest.objects.filter(to_user=profile)


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        profile = Profile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id=None):
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


class ProfileFriends(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileFriendsSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        profile = Profile.objects.get(id=id)
        friends = profile.friends.all()
        serializer = ProfileSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
