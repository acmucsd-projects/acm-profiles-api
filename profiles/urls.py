from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import include

user_router = DefaultRouter()
user_router.register(r'profile', ProfileViewSet)
user_router.register(r'settings', SettingViewSet)
user_router.register(r'socials', UserSocialViewSet)

urlpatterns = [
    path('user/', include(user_router.urls)),
    path('follower/<str:following>/', FollowerView.as_view()),
    path('following/<str:follower>/', FollowingView.as_view()),
    path('community_membership/<str:member>/', Community_MembershipView.as_view()),
    path('communities/', CommunitiesView_LC.as_view()),
    path('communities/<str:pk>/', CommunitiesView_RUD.as_view()),
    path('community_member/', CommunityMemberView_LC.as_view()),
    path('community_member/<str:pk>/', CommunityMemberView_RUD.as_view()),
    path('community_social/', CommunitySocialView_C.as_view()),
    path('community_social/<str:pk>/', CommunitySocialView_RUD.as_view()),
]