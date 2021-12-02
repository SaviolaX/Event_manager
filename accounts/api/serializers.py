from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import Profile, FriendRequest
from events.models import EventInviteRequest


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class EventInviteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInviteRequest
        fields = '__all__'


class FriendRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('from_user', 'to_user', 'timestamp',)


class ProfileFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('friends',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserViewSerializer(read_only=True)
    friends = ProfileFriendsSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'city', 'photo', 'friends')


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    password = serializers.CharField(max_length=68,
                                     min_length=6,
                                     write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        """Get attrs and check alphanumeric"""
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should contain only alphanumeric characters')
        return attrs

    def create(self, validated_data):
        """Create user and profile"""
        create_user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=create_user)
        return create_user
