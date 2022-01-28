from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from ..models import Profile, FriendRequest
from events.models import EventInviteRequest, Event
from events.api.serializers import EventSerializer
from .serializers import (RegisterSerializer, ProfileSerializer)


def decline_event_invite_request(request, profile_id, req_id):
    profile = Profile.objects.get(id=profile_id)
    e_request = EventInviteRequest.objects.get(id=req_id)
    if e_request.to_profile == request.user.profile:
        e_request.delete()
        return Response('Event invitation was canceled successfully',
                        status=status.HTTP_200_OK)
    else:
        return Response('You can not cancel invitation, it is not yours',
                        status=status.HTTP_403_FORBIDDEN)


def accept_event_invite_request(request, profile_id, req_id):
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


def get_all_profile_friends(request, id):
    profile = Profile.objects.get(id=id)
    friends = profile.friends.all()
    serializer = ProfileSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def cancel_friend_request(request, id):
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


def decline_friend_request(request, req_id, profile_id):
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


def accept_friend_request(request, req_id, profile_id):
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


def create_friend_request(request, id):
    try:
        to_user = get_object_or_404(Profile, id=id)
        profile = Profile.objects.get(user=request.user)
        f_request, created = FriendRequest.objects.get_or_create(
            from_user=profile,
            to_user=to_user)
        return Response({'create friend request': True})
    except FriendRequest.DoesNotExist:
        return Response({'Something happened with function': True})


def delete_friend(request, profile_id, friend_id):
    profile = Profile.objects.get(id=profile_id)
    friend = profile.friends.get(id=friend_id)
    profile.friends.remove(friend)
    friend.friends.remove(profile)
    return Response({'delete friend': True})


def get_profile_event_list(request, id):
    profile = Profile.objects.get(id=id)
    events = Event.objects.all().filter(creator=profile)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_profile_page(request, id):
    try:
        profile = Profile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response('Profile does not exist, wrong address',
                        status=status.HTTP_403_FORBIDDEN)


def edit_profile_page(request, id):
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
        return Response('You can not edit profile',
                        status=status.HTTP_403_FORBIDDEN)


def register_user(request):
    user = request.data
    serializer = RegisterSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_data = serializer.data

    return Response(user_data, status=status.HTTP_201_CREATED)
