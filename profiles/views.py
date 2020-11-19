from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.

class ProfileView(generics.ListCreateAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer

class SettingsView(generics.ListCreateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class FollowingView(generics.ListCreateAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class CommunitiesView(generics.ListCreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

class CommunityMemberView(generics.ListCreateAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer

class CommunitySocialView(generics.ListCreateAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class UserSocialView(generics.ListCreateAPIView):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer
