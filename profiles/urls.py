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
    path('community/search/', CommunitiesSearchView.as_view()),
    path('community/create/<str:uuid>/', CommunitiesCreateView.as_view()),
    path('community/<str:ucid>/add-admin/<str:member>/<str:admin>/', CommunityMemberView_RU.as_view()),
    path('community/edit/<str:ucid>/<str:uuid>/', CommunitiesView_RUD.as_view()),
    path('community/members/<str:ucid>', Member_ListView.as_view()),
    path('community_list/<str:uuid>/', Community_ListView.as_view()),
    path('community_social/', CommunitySocialView_C.as_view()),
    path('community_social/<str:pk>/', CommunitySocialView_RUD.as_view()),
]