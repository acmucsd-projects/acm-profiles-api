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
    path('community_search/', CommunitiesSearchView.as_view()),
    path('create_community/', CommunitiesCreateView.as_view()),
    path('communities/<str:ucid>/<str:uuid>/', CommunitiesView_RUD.as_view()),
    path('member_list/<str:ucid>', Member_ListView.as_view()),
    path('community_list/<str:uuid>/', Community_ListView.as_view()),
    path('community_members/<str:pk>/', CommunityMemberView_RUD.as_view()),
    path('community_social/', CommunitySocialView_C.as_view()),
    path('community_social/<str:pk>/', CommunitySocialView_RUD.as_view()),
]