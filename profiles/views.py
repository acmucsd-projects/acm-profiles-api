from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics, filters, mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import *
from .serializers import *

"""
Search by name or socials.
Filter by profile visibility from profile settings
"""
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

"""
CRUD for user settings
"""
class SettingViewSet(ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

"""
Given uuid, returns uuid's of users who follow them
"""
class FollowerView(generics.ListAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowerListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("following")
        queryset = User_following.objects.filter(following=uuid)
        return queryset

"""
Given uuid, returns uuid's of users who they follow
"""
class FollowingView(generics.ListAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("follower")
        queryset = User_following.objects.filter(follower=uuid)
        return queryset

"""
Lists communities
Search by community name
Filter by if community is active
"""
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

"""
Create a community
"""
class CommunitiesCreateView(generics.CreateAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer

"""
Checks if user is admin of the community.
If yes, accepts the update/delete request
"""
class CommunitiesView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        membership_queryset = Community_members.objects.all()
        filter = {}
        membership_filter = {}
        for field in self.kwargs:
            if (field == "ucid"):
                filter[field] = self.kwargs[field]
        for field in self.kwargs:
            if self.kwargs[field]:
                if field == "ucid":
                    membership_filter[field] = self.kwargs[field]
                else:
                    membership_filter["member_id"] = self.kwargs[field]
        admin_obj = get_object_or_404(membership_queryset, **membership_filter)
        if admin_obj.admin:  
            obj = get_object_or_404(queryset, **filter)
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404("User is not an admin")

"""
Given ucid, returns uuid's and admin status of members with admins on top
"""
class Member_ListView(generics.ListAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer
    def get_queryset(self):
        ucid = self.kwargs.get("ucid")
        queryset = Community_members.objects.filter(ucid=ucid).order_by('-admin')
        return queryset

"""
Given uuid, returns ucid's of community's the user holds membership to
"""
class Community_ListView(generics.ListAPIView):
    queryset = Community_members.objects.all()
    serializer_class = Community_MembershipSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        queryset = Community_members.objects.filter(member_id=uuid)
        return queryset

"""
Given ucid, an admin's uuid, and a member id, can make the member an admin

Raises error if 
1. The expected admin and/or member are not part of the community
2. The individual adding an admin is not an admin
3. The individual being added as an admin is already an admin
"""
class CommunityMemberView_RU(generics.RetrieveUpdateAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        member_filter = {}
        admin_filter = {}
        for field in self.kwargs:
            if (field == "ucid"):
                member_filter[field] = self.kwargs[field]
                admin_filter[field] = self.kwargs[field]
            if (field == "member"):
                member_filter["member_id"] = self.kwargs[field]
            if (field == "admin"):
                admin_filter["member_id"] = self.kwargs[field]
        admin_obj = get_object_or_404(queryset, **admin_filter)
        if admin_obj.admin:
            member_obj = get_object_or_404(queryset, **member_filter) 
            if member_obj.admin:
                raise Http404("Member is already admin") 
            self.check_object_permissions(self.request, member_obj)
            return member_obj
        raise Http404("Only an admin can add other admins")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.admin = True
        instance.save()
        return Response(serializer.data)

class CommunitySocialView_C(generics.CreateAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class CommunitySocialView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

class UserSocialViewSet(ModelViewSet):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer

