from django.contrib.auth.decorators import login_required

from .event_settings_logic import *
from .event_invitation_logic import *
from .join_event_logic import *
from .event_page_logic import *



def all_events(request):
    """Display all open events"""
    return get_all_open_events(request)



def event_page(request, id):
    """Show event page"""
    return get_event_page(request, id)



def kick_event_participators(request, id, profile_id):
    """Remove profile from event participators list"""
    return kick_participator_from_event(request, id, profile_id)



def profiles_list_for_inviting_to_event(request, event_id):
    """Display list of all users you can invite"""
    return get_list_of_all_users(request, event_id)



def invite_to_event_from_list_of_all_users(request, event_id, profile_id):
    """Send invite from event to user to join event ONLY FOR ALL USERS
    redirect to the same list of all users"""
    event_sends_invite_request_to_user(request, event_id, profile_id)
    return redirect('events:invite_people', event_id)



def cancels_invite_request_to_user_from_list_all_of_users(request,
                                                          event_id,
                                                          profile_id):
    """Cancel invite event request and redirects to list of all users"""
    return event_cancels_invite_request_to_user(request, event_id, profile_id)



def friends_list_for_inviting_to_event(request, event_id):
    """Display list of all your friends you can invite"""
    return get_list_of_all_friends(request, event_id)



def invite_to_event_from_list_of_all_friends(request, event_id, profile_id):
    """Send invite from event to FRIEND to join event ONLY FOR FRIENDS
    redirect to the same list of all friends"""
    event_sends_invite_request_to_user(request, event_id, profile_id)
    return redirect('events:invite_friends', event_id)



def cancels_invite_request_to_friend_from_list_all_of_friends(request,
                                                              event_id,
                                                              profile_id):
    """Cancel invite event request and redirects to list of all friends"""
    event_cancels_invite_request_to_user(request, event_id, profile_id)
    return redirect('events:invite_friends', event_id)



def from_event_to_user_invite_request(request, event_id, profile_id):
    """Send invite from event to user to join event"""
    return event_sends_invite_request_to_user(request, event_id, profile_id)



def join_event(request, id):
    """Join event without any request"""
    return instantly_join_event_without_requests(request, id)



def request_join_event(request, event_id):
    """Create request USER --> EVENT"""
    return user_sends_create_request_to_join_event(request, event_id)



def cancel_join_request(request, id):
    """Cancel request to join event"""
    return cancel_and_delete_join_request(request, id=id)



def accept_join_event_request(request, id):
    """Add user to event participators"""
    return add_user_to_event_participators(request, id)



def decline_join_event_request(request, id):
    """Decline and delete request"""
    return decline_to_join_then_delete_request(request, id)



def leave_event(request, id):
    """Remove user from event participators"""
    return remove_user_from_event_participators(request, id)



def accept_event_invite(request, id):
    """Add user to event participators"""
    return accept_invitation(request, id)



def decline_event_invite(request, id):
    """Decline and delete invite request"""
    return decline_invitation(request, id)



def create_event(request):
    """Create event"""
    return create_event_and_assign_to_current_user(request)



def edit_event(request, id):
    """Edit event information"""
    return edit_current_event(request, id)



def delete_event(request, id):
    """Delete event"""
    return delete_current_event(request, id)
