from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *

# Create your views here.

class ProfileView(generics.CreateAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfileSerializer

class SettingsView(generics.CreateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class FollowingView(generics.CreateAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingSerializer

class CommunitiesView(generics.CreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

class CommunityMemberView(generics.CreateAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer

class CommunitySocialView(generics.CreateAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class UserSocialView(generics.CreateAPIView):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer
