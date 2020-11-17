from django.urls import path
from .views import *

urlpatterns = [
    path('profile', ProfileView.as_view()),
    path('settings', SettingsView.as_view()),
    path('following', FollowingView.as_view()),
    path('communities', CommunitiesView.as_view()),
    path('community_member', CommunityMemberView.as_view()),
    path('community_social', CommunitySocialView.as_view()),
    path('user_social', UserSocialView.as_view())
]