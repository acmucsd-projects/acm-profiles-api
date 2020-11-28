from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView_LC.as_view()),
    path('profile/<int:pk>/', ProfileView_RUD.as_view()),
    path('settings/', SettingView_C.as_view()),
    path('settings/<int:pk>/', SettingView_RUD.as_view()),
    path('following/', FollowingView_LC.as_view()),
    path('following/<int:pk>/', FollowingView_RD.as_view()),
    path('communities/', CommunitiesView_LC.as_view()),
    path('communities/<int:pk>/', CommunitiesView_RUD.as_view()),
    path('community_member/', CommunityMemberView_LC.as_view()),
    path('community_member/<int:pk>/', CommunityMemberView_RUD.as_view()),
    path('community_social/', CommunitySocialView_C.as_view()),
    path('community_social/<int:pk>/', CommunitySocialView_RUD.as_view()),
    path('user_social/', UserSocialView_LC.as_view()),
    path('user_social/<int:pk>/', UserSocialView_RUD.as_view())
]