from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'settings', SettingViewSet)

urlpatterns = [
    path('user/', include(router.urls)),
    path('follower/<str:following>/', FollowerView.as_view()),
    path('following/<str:follower>/', FollowingView.as_view()),
    path('communities/', CommunitiesView_LC.as_view()),
    path('communities/<str:pk>/', CommunitiesView_RUD.as_view()),
    path('community_member/', CommunityMemberView_LC.as_view()),
    path('community_member/<str:pk>/', CommunityMemberView_RUD.as_view()),
    path('community_social/', CommunitySocialView_C.as_view()),
    path('community_social/<str:pk>/', CommunitySocialView_RUD.as_view()),
    path('user_social/', UserSocialView_LC.as_view()),
    path('user_social/<str:pk>/', UserSocialView_RUD.as_view())
]