from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class Friendship(models.Model):
    user1 = models.ForeignKey(CustomUser, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name='friendship_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def accept(self):
        self.accepted_at = timezone.now()
        self.save()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friends request sent from {self.from_user} to {self.to_user} on {self.created_at}"