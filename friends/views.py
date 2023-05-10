import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from friends.models import FriendRequest, Friendship
from friends.serializers import FriendRequestSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('user_id')
    to_user = get_object_or_404(CustomUser, id=to_user_id)
    from_user = request.user

    # Check if the user has already received a friend request from the same user
    if FriendRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
        # Accept the request.
        request = FriendRequest.objects.filter(from_user=to_user, to_user=from_user).first()
        request.accepted = True
        request.save()
        return Response({"error": "Friend request already received from this user. which is now accepted."}, status=400)

    # Check if the friend request has already been sent
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({"error": "Friend request already sent."}, status=400)

    # Check if the user has sent more than 3 friend requests in the past hour
    now = timezone.now()
    hour_ago = now - datetime.timedelta(hours=1)
    friend_requests_sent = FriendRequest.objects.filter(from_user=from_user, created_at__gte=hour_ago)
    if friend_requests_sent.count() >= 3:
        return Response({"error": "You have reached the limit of sending 3 friend requests per hour."}, status=400)

    # Create the friend request
    friend_request = FriendRequest(from_user=from_user, to_user=to_user)
    friend_request.save()

    return Response({"success": "Friend request sent."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    friend_request_id = request.data.get('friend_request_id')
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, to_user=request.user)

    # Delete the friend request
    friend_request.delete()

    return Response({"success": "Friend request rejected."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    friend_request_id = request.data.get('friend_request_id')
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, to_user=request.user)

    # Create a new Friendship object
    friendship = Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
    friendship.accept()

    # Delete the friend request
    friend_request.delete()

    return Response({"success": "Friend request accepted."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_friend_requests(request):
    # Get all friend requests received by the authenticated user
    friend_requests_received = FriendRequest.objects.filter(to_user=request.user, accepted=False)

    # Serialize the friend requests received
    serializer = FriendRequestSerializer(friend_requests_received, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    user = request.user

    # Filter friendships where the user is either the sender or the receiver and the friendship is accepted
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user), accepted_at__isnull=False)

    # Get the friend objects from the friendships
    friends = [friendship.user1 if friendship.user2 == user else friendship.user2 for friendship in friendships]

    # Serialize the friend objects
    serializer = CustomUserSerializer(friends, many=True)

    return Response(serializer.data)