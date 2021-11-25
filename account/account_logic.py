from django.shortcuts import render, redirect

from .models import Profile, FriendRequest
from events.models import EventInviteRequest, Event


def get_all_profiles_list(request):
    """Gets all profiles from database"""
    profiles = Profile.objects.all()

    context = {'profiles': profiles}
    return render(request, 'account/all_profiles.html', context)


def get_profile_all_friends(request):
    """Gets all friends of current user profile"""
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    return friends


def get_user_profile_page(request, id):
    """Gets profile and it's friends,
    also get friend request to this profile
    """
    profile = Profile.objects.get(id=id)
    friends = profile.friends.all()
    friend_invite = FriendRequest.objects.filter(to_user=profile).first()

    context = {'profile': profile, 'friends': friends,
               'friend_invite': friend_invite}
    return render(request, 'account/profile.html', context)


def get_profiles_friends_list(request, id):
    """Gets profile's friends list and show all friend requests"""
    profile = Profile.objects.get(id=id)
    friends = profile.friends.all()
    recieved_request = FriendRequest.objects.filter(to_user=profile)

    context = {'profile': profile,
               'friends': friends,
               'recieved_request': recieved_request}
    return render(request, 'account/friends_list.html', context)


def get_all_my_events(request):
    """
        Gets all events made by current user profile.
        Gets all events current user takes part in.
        Gets all invites sent by events to take a part in ones.
    """
    profile = Profile.objects.get(user=request.user)
    events = Event.objects.all().filter(creator=profile)
    take_part_events = Event.objects.all().filter(participators=profile)
    event_invites = EventInviteRequest.objects.filter(to_profile=profile)

    context = {'events': events, 'profile': profile,
               'event_invites': event_invites,
               'take_part_events': take_part_events}
    return render(request, 'account/my_events.html', context)


def create_friend_request(request, from_user, to_user):
    """
    Creates a friend request between current user profile and
    another profile
    """
    f_request, created = FriendRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user)
    return f_request, created


def creating_and_sending_friend_request(request, id):
    """Initializes 2 profiles and create friend request between them"""
    profile = Profile.objects.get(user=request.user)
    to_user = Profile.objects.get(id=id)
    f_request, created = create_friend_request(
        request, from_user=profile, to_user=to_user)

    return redirect('account:profile', to_user.id)


def delete_user_from_friend_list(request, id):
    """Removes profiles from each others friends lists"""
    profile = Profile.objects.get(user=request.user)
    friend = Profile.objects.get(id=id)
    profile.friends.remove(friend)
    friend.friends.remove(profile)

    return redirect('account:friends_list', profile.id)


def accept_request(request, id):
    """Accepts friend request and add each other to friends lists"""
    f_request = FriendRequest.objects.get(id=id)
    if f_request.to_user == request.user.profile:
        f_request.to_user.friends.add(f_request.from_user)
        f_request.from_user.friends.add(f_request.to_user)
        f_request.delete()
        return redirect('account:friends_list', request.user.profile.id)


def decline_request(request, id):
    """Declines friend request and delete request"""
    f_request = FriendRequest.objects.get(id=id)
    if f_request.to_user == request.user.profile:
        f_request.delete()
    elif f_request.from_user == request.user.profile:
        f_request.delete()
        return redirect('account:friends_list', request.user.profile.id)


def cancel_request(request, id):
    """Cancels request that was sent to profile"""
    profile = Profile.objects.get(id=id)
    sent_requests = FriendRequest.objects.filter(
        from_user=request.user.profile, to_user=profile).first()
    if sent_requests.from_user == request.user.profile:
        sent_requests.delete()
        return redirect('account:profile', profile.id)
