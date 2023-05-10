from django.urls import path

from accounts.views import signup, login_view, search_users


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('search/', search_users, name="user_search")
]
