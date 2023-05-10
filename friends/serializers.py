from rest_framework import serializers

from friends.models import FriendRequest, Friendship


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id' ,'from_user', 'accepted', 'created_at')
