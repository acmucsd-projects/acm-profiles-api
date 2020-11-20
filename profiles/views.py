from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.

class ProfileView_LC(generics.ListCreateAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer

class ProfileView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer

class SettingView_C(generics.CreateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class SettingView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class FollowingView_LC(generics.ListCreateAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class FollowingView_RD(generics.RetrieveDestroyAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class CommunitiesView_LC(generics.ListCreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

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
