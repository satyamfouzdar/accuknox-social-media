from django.contrib import admin

from friends.models import FriendRequest, Friendship

admin.site.register(Friendship)

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'accepted', 'created_at')
