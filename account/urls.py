from django.urls import path, include

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.account_registration, name='register'),

    # Django authentication system
    path('', include('django.contrib.auth.urls')),

    # Profile
    path('profiles/', views.all_profiles, name='all_profiles'),
    path('profile/<int:id>/', views.user_profile, name='profile'),
    path('edit_profile/<int:id>/', views.edit_profile, name='edit_profile'),
    path('<int:id>/friends_list/', views.user_friends_list,
         name='friends_list'),
    path('my_events/', views.my_events, name='my_events'),


    # Request controllers
    path('send_friend_request/<int:id>/',
         views.send_friend_request, name='send'),
    path('accept_friend_request/<int:id>/',
         views.accept_friend_request, name='accept'),
    path('cancel_friend_request/<int:id>/',
         views.cancel_friend_request, name='cancel'),
    path('delete_friend/<int:id>/', views.delete_friend,
         name='delete'),
    path('cancel_sending_friend_request/<int:id>/',
         views.cancel_sending_friend_request,
         name='cancel_sending_request'),
]
