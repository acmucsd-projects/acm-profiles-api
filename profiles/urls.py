from django.urls import path
from .views import *
from django.urls import include

urlpatterns = [
    path('user/login', LoginView.as_view()),
    path('user/profile/<uuid:user>', ProfileView.as_view()),
    path('user/profile/search', ProfileSearch.as_view()),
    path('user/profile/settings/<uuid:user>', UserSettingsView.as_view()),
    path('user/profile/socials/<uuid:user>', UserSocialView.as_view()),
    path('user/recommendations/<uuid:user>', RecommendationsView.as_view()),
    path('user/follower_list/<uuid:following>', FollowerView.as_view()),
    path('user/following_list/<uuid:follower>', FollowingView.as_view()),
    path('user/follow/<uuid:follower>/<uuid:following>', UserFollowView.as_view()),
    path('user/unfollow/<uuid:follower>/<uuid:following>', UserUnfollowView.as_view()),
    path('user/community_list/<uuid:member>', CommunityListView.as_view()),
    path('community/<uuid:community>', CommunityView.as_view()),
    path('community/search', CommunitiesSearchView.as_view()),
    path('community/create/<uuid:user>', CommunitiesCreateView.as_view()),
    path('community/edit/<uuid:community>/<uuid:admin>', EditCommunityView.as_view()),
    path('community/member_list/<uuid:community>', MemberListView.as_view()),
    path('community/social/<uuid:community>', CommunitySocialView.as_view()),
    path('community/social/<uuid:community>/<uuid:admin>', EditCommunitySocialView.as_view()),
    path('community/<uuid:community>/add-admin/<uuid:member>/<uuid:admin>', AddAdminView.as_view()),
    path('community/<uuid:community>/join/<uuid:user>', JoinCommunityView.as_view()),
    path('community/<uuid:community>/leave/<uuid:member>', LeaveCommunityView.as_view()),
]