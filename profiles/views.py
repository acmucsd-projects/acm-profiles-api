from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics, filters, mixins, status
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        uuid = request.data.get("uuid")
        user = Profiles.objects.get(uuid=uuid)
        self.addRecommendations(uuid, user.major, user.grad_year)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def addRecommendations(self, id, major, grad_year):
        profiles = Profiles.objects.exclude(uuid=id)
        for e in profiles:
            similarity = 0
            if major != "" and e.major == major:
                similarity += 1
            if grad_year is not None and e.grad_year == grad_year:
                similarity += 1
            recommendation = Recommendations(user=Profiles.objects.get(uuid=id), recommendation=e, similarity=similarity)
            recommendation.save()
            recommendation = Recommendations(user=e, recommendation=Profiles.objects.get(uuid=id), similarity=similarity)
            recommendation.save()


"""
CRUD for user settings
"""
class SettingViewSet(ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

"""
CRUD for user socials
"""
class UserSocialViewSet(ModelViewSet):
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer

"""
List of recommendations based on similarity
"""
class RecommendationsView(generics.ListAPIView):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        queryset = Recommendations.objects.filter(user=uuid).order_by('-similarity')[:5]
        return queryset

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
Creates a follower relation given uuid's of two users
"""
class UserFollowView(generics.CreateAPIView):
    queryset = User_following.objects.all()
    serializer_class = FollowingEmptySerializer
    def post(self, request, *args, **kwargs):
        follow = User_following(follower=Profiles.objects.get(uuid=kwargs["follower"]), following=Profiles.objects.get(uuid=kwargs["following"]))
        follow.save()
        return Response(status=status.HTTP_201_CREATED)

"""
Removes follower relation given uuid's of two users
"""
class UserUnfollowView(generics.DestroyAPIView):
    queryset = User_following.objects.all()
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"follower" : self.kwargs["follower"],
                  "following" : self.kwargs["following"]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

"""
Given uuid, returns ucid's of community's the user holds membership to
"""
class Community_ListView(generics.ListAPIView):
    queryset = Community_members.objects.all()
    serializer_class = CommunityListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("uuid")
        queryset = Community_members.objects.filter(member_id=uuid)
        return queryset

"""
Lists communities
Search by community name
Filter by if community is active
"""
class CommunitiesSearchView(generics.ListAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesDisplaySerializer
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
    serializer_class = CommunitiesCreateSerializer
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        community = Communities.objects.get(title=request.data.get("title"))
        member = Profiles.objects.get(uuid=kwargs.get("uuid"))
        membership = Community_members(ucid=community, member_id=member, admin=True)
        membership.save()
        return response

"""
Checks if user is admin of the community.
If yes, accepts the update/delete request
"""
class CommunitiesView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Communities.objects.all()
    serializer_class = CommunitiesCreateSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        membership_queryset = Community_members.objects.all()
        filter = {}
        membership_filter = {}
        for field in self.kwargs:
            if self.kwargs[field]:
                if field == "ucid":
                    membership_filter[field] = self.kwargs[field]
                    filter[field] = self.kwargs[field]
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
    serializer_class = MemberListSerializer
    def get_queryset(self):
        ucid = self.kwargs.get("ucid")
        queryset = Community_members.objects.filter(ucid=ucid).order_by('-admin')
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

class JoinCommunityView(generics.CreateAPIView):
    queryset = Community_members.objects.all()
    serializer_class = JoinCommunityMemberSerializer
    def post(self, request, *args, **kwargs):
        member = Community_members(ucid=Communities.objects.get(ucid=kwargs["ucid"]), member_id=Profiles.objects.get(uuid=kwargs["uuid"]), admin=False)
        member.save()
        updateRecommendations(kwargs["uuid"], kwargs["ucid"], 1)
        return Response(status=status.HTTP_201_CREATED)

class LeaveCommunityView(generics.DestroyAPIView):
    queryset = Community_members.objects.all()
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"ucid" : self.kwargs["ucid"],
                  "member_id" : self.kwargs["uuid"]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        updateRecommendations(kwargs["uuid"], kwargs["ucid"], -1)
        return response

"""
Function to update recommendations when a user joins or leaves a commmunity
"""
def updateRecommendations(user, community, change):
    membership_queryset = Community_members.objects.filter(ucid=community).exclude(member_id=user)
    for e in membership_queryset:
        recommendation = Recommendations.objects.get(user=user, recommendation=e.member_id)
        recommendation.similarity += change
        recommendation.save()
        recommendation = Recommendations.objects.get(user=e.member_id, recommendation=user)
        recommendation.similarity += change
        recommendation.save()

"""
Creates community socials
"""
class CommunitySocialView_C(generics.CreateAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer

"""
Updates the community socials if requested by admin
"""
class CommunitySocialView_RUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community_socials.objects.all()
    serializer_class = CommunitySocialSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        membership_queryset = Community_members.objects.all()
        filter = {}
        membership_filter = {}
        for field in self.kwargs:
            if self.kwargs[field]:
                if field == "ucid":
                    membership_filter[field] = self.kwargs[field]
                    filter[field] = self.kwargs[field]
                else:
                    membership_filter["member_id"] = self.kwargs[field]
        admin_obj = get_object_or_404(membership_queryset, **membership_filter)
        if admin_obj.admin:  
            obj = get_object_or_404(queryset, **filter)
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404("User is not an admin")

