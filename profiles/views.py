from django.shortcuts import render, get_object_or_404
from django.http import Http404
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

class CommunitiesSearchView(generics.ListAPIView):
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

class CommunitiesCreateView(generics.CreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

class CommunitiesView_UD(generics.UpdateDestroyAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        queryset2 = Community_members.objects.all()
        filter = {}
        filter2 = {}
        for field in self.kwargs:
            if (field == "ucid"):
                filter[field] = self.kwargs[field]
        for field in self.kwargs:
            if self.kwargs[field]:
                if field == "ucid":
                    filter2[field] = self.kwargs[field]
                else:
                    filter2["member_id"] = self.kwargs[field]
        admin_obj = get_object_or_404(queryset2, **filter2)
        if admin_obj.admin:  
            obj = get_object_or_404(queryset, **filter)
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404("User is not an admin")

class Community_MembershipView(generics.ListAPIView):
    queryset = Community_members.objects.all()
    serializer_class = Community_MembershipSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("member")
        queryset = Community_members.objects.filter(member_id=uuid)
        return queryset

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

class UserSocialViewSet(ModelViewSet):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer

