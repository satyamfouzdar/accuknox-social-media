from django.urls import path

from friends.views import send_friend_request, reject_friend_request, list_pending_friend_requests, accept_friend_request, list_friends


urlpatterns = [
    path('send-friend-request/', send_friend_request, name='send_friend_request'),
    path('reject-friend-request/', reject_friend_request, name="reject_friend_request"),
    path('accept-friend-request/', accept_friend_request, name="accept_friend_request"),
    path('pending-requests/', list_pending_friend_requests, name="pending-requests"),
    path('list-friends/', list_friends, name='list_friends')
]
