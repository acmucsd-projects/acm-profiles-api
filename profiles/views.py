from django.shortcuts import render
from rest_framework import generics, filters, mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import *
from .serializers import *

# Create your views here.
class ProfileViewSet(ModelViewSet):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'socials__discord',
    'socials__snapchat', 'socials__github', 'socials__email']
    def get_queryset(self):
        queryset = Profiles.objects.all()
        visibility = self.request.query_params.get('vis', None)
        if visibility is not None:
            queryset = queryset.filter(settings__profile_visibility=visibility)
        return queryset

class SettingViewSet(ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer


class FollowerView(generics.ListAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowerListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("following")
        queryset = User_following.objects.filter(following=uuid)
        return queryset
    

class FollowingView(generics.ListAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("follower")
        queryset = User_following.objects.filter(follower=uuid)
        return queryset

class FollowingView_LC(generics.ListCreateAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class FollowingView_RD(generics.RetrieveDestroyAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class CommunitiesView_LC(generics.ListCreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'socials__discord', 'socials__instagram']
    def get_queryset(self):
        queryset = Communities.objects.all()
        visibility = self.request.query_params.get('vis', None)
        if visibility is not None:
            queryset = queryset.filter(active=visibility)
        return queryset

class CommunitiesView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

class CommunityMemberView_LC(generics.ListCreateAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer

class CommunityMemberView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer

class CommunitySocialView_C(generics.CreateAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class CommunitySocialView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class UserSocialView_LC(generics.ListCreateAPIView):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer

class UserSocialView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer
