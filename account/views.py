from django.contrib.auth.decorators import login_required

from .account_logic import *
from .account_registration_and_edit_logic import *


def all_profiles(request):
    """Get list of all profiles"""
    return get_all_profiles_list(request)


@login_required
def user_profile(request, id):
    """ User's profile """
    return get_user_profile_page(request, id)


def edit_profile(request, id):
    """Edit current profile"""
    return edit_current_profile_account(request, id)


@login_required
def user_friends_list(request, id):
    """ User's frinends list and firends requests """
    return get_profiles_friends_list(request, id)


def my_events(request):
    """Get all current profile's events"""
    return get_all_my_events(request)


@login_required
def send_friend_request(request, id):
    """ Send a friend request """
    return creating_and_sending_friend_request(request, id)


@login_required
def delete_friend(request, id):
    """ Delete friend """
    return delete_user_from_friend_list(request, id)


@login_required
def accept_friend_request(request, id):
    """ Accept friend request """
    return accept_request(request, id)


@login_required
def cancel_friend_request(request, id):
    """ Decline friend request """
    return decline_request(request, id)


def cancel_sending_friend_request(request, id):
    """Cancel friend request"""
    return cancel_request(request, id)


def account_registration(request):
    """Registration"""
    return register(request)
