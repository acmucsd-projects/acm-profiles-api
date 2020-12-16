from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import generics, filters, mixins, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import *
from .serializers import *
import requests

PORTAL_URL = ''
PORTAL_USER_URL = PORTAL_URL + "/api/v2/user"

class ProfileViewSet(ModelViewSet):
    """
    Search by name or socials.
    Filter by profile visibility from profile settings
    Creates socials and settings
    Creates recommendation entries
    """
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
        settings = Settings(user=user)
        settings.save()
        socials = User_socials(user=user)
        socials.save()
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

    def perform_create(self, request):
        """parsing json objects from portal API calls and adding them"""
        data = request.data
        payload = {'email': data['email'], 'password': data['password']}
        headers= {}

        response = requests.request('POST', PORTAL_USER_URL, headers=headers, data = payload)
        if response['error'] != None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        present = Profiles.objects.filter_by(uuid=response['user']['uuid']).first()
        
        if present == None:
            payload={}
            portal_user = requests.request('POST', PORTAL_USER_URL, headers={"Authorization": f"Bearer {r['token']}"}, data=payload)['user']
            user = Profiles(
                uuid = portal_user['uuid'],
                email = portal_user['email'],
                first_name = portal_user['firstName'],
                last_name = portal_user['lastName'],
                major = portal_user['major'],
                grad_year = portal_user['graduationYear'],
                profile_pic = portal_user['profilePicture'],
            )
            user.save()
            return Response(status=status.HTTP_201_CREATED)

class UserSettingsView(generics.RetrieveUpdateAPIView):
    """
    Can retrieve and update user's settings given their uuid
    """
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"user" : self.kwargs.get("user")}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class UserSocialView(generics.RetrieveUpdateAPIView):
    """
    Can retrieve and update user's socials given their uuid
    """
    queryset = User_socials.objects.all()
    serializer_class = UserSocialSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"user" : self.kwargs.get("user")}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RecommendationsView(generics.ListAPIView):
    """
    User's recommendation list
    Doesn't recommend individuals the user is already following
    Sends top five results order in descending order of similarity
    """
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("user")
        recommendation_queryset = Recommendations.objects.filter(user=uuid)
        following_queryset = User_following.objects.filter(follower=uuid)
        for following in following_queryset:
            recommendation_queryset.exclude(recommendation=following.following)
        return recommendation_queryset.order_by('-similarity')[:5]

class FollowerView(generics.ListAPIView):
    """
    Given uuid returns uuids of users who follow them
    """
    queryset = User_following.objects.all()
    serializer_class = FollowerListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("following")
        queryset = User_following.objects.filter(following=uuid)
        return queryset

class FollowingView(generics.ListAPIView):
    """
    Given uuid returns uuids of users who they follow
    """
    queryset = User_following.objects.all()
    serializer_class = FollowingListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("follower")
        queryset = User_following.objects.filter(follower=uuid)
        return queryset

class UserFollowView(generics.CreateAPIView):
    """
    Creates a follower relation given uuids of two users
    """
    queryset = User_following.objects.all()
    serializer_class = FollowingEmptySerializer
    def post(self, request, *args, **kwargs):
        follow = User_following(follower=Profiles.objects.get(uuid=kwargs["follower"]), following=Profiles.objects.get(uuid=kwargs["following"]))
        follow.save()
        return Response(status=status.HTTP_201_CREATED)

class UserUnfollowView(generics.DestroyAPIView):
    """
    Removes follower relation given the uuids of two users
    """
    queryset = User_following.objects.all()
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"follower" : self.kwargs["follower"],
                  "following" : self.kwargs["following"]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class CommunityListView(generics.ListAPIView):
    """
    Given uuid, returns the ids of communities the user holds membership to
    """
    queryset = Community_members.objects.all()
    serializer_class = CommunityListSerializer
    def get_queryset(self):
        uuid = self.kwargs.get("member")
        queryset = Community_members.objects.filter(member=uuid)
        return queryset

class CommunitiesSearchView(generics.ListAPIView):
    """
    Lists communities
    Search by community name
    Filter by if community is active
    """
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

class CommunitiesCreateView(generics.CreateAPIView):
    """
    Create a community
    Create socials for the community
    Makes the community creator an admin
    """
    queryset = Communities.objects.all()
    serializer_class = CommunitiesCreateSerializer
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        community = Communities.objects.get(title=request.data.get("title"))
        member = Profiles.objects.get(uuid=kwargs.get("user"))
        membership = Community_members(community=community, member=member, admin=True)
        membership.save()
        socials = Community_socials(community=community)
        socials.save()
        return response

class EditCommunityView(generics.RetrieveUpdateDestroyAPIView):
    """
    Checks if user is admin of the community.
    If yes, allows for updating/deleting the community.
    """
    queryset = Communities.objects.all()
    serializer_class = CommunitiesCreateSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        membership_queryset = Community_members.objects.all()
        filter = {}
        membership_filter = {}
        membership_filter["community"] = self.kwargs["community"]
        membership_filter["member"] = self.kwargs["admin"]
        admin_obj = get_object_or_404(membership_queryset, **membership_filter)
        if admin_obj.admin:  
            obj = get_object_or_404(queryset, **filter)
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404("User is not an admin")

class MemberListView(generics.ListAPIView):
    """
    Given the community id, returns uuids and admin status of members with admins on top
    """
    queryset = Community_members.objects.all()
    serializer_class = MemberListSerializer
    def get_queryset(self):
        ucid = self.kwargs.get("community")
        queryset = Community_members.objects.filter(community=ucid).order_by('-admin')
        return queryset

class AddAdminView(generics.RetrieveUpdateAPIView):
    """
    Given ucid, an admin's uuid, and a member id, can make the member an admin

    Raises error if 
    1. The expected admin and/or member are not part of the community
    2. The individual adding an admin is not an admin
    3. The individual being added as an admin is already an admin
    """
    queryset = Community_members.objects.all()
    serializer_class = CommunityMemberSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        member_filter = {}
        admin_filter = {}
        for field in self.kwargs:
            if (field == "community"):
                member_filter[field] = self.kwargs[field]
                admin_filter[field] = self.kwargs[field]
            if (field == "member"):
                member_filter["member"] = self.kwargs[field]
            if (field == "admin"):
                admin_filter["member"] = self.kwargs[field]
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
    """
    Given uuid and commmunity id, adds the user to 
    the community.
    """
    queryset = Community_members.objects.all()
    serializer_class = JoinCommunityMemberSerializer
    def post(self, request, *args, **kwargs):
        member = Community_members(community=Communities.objects.get(ucid=kwargs["community"]), member=Profiles.objects.get(uuid=kwargs["user"]), admin=False)
        member.save()
        updateRecommendations(kwargs["user"], kwargs["community"], 1)
        return Response(status=status.HTTP_201_CREATED)

class LeaveCommunityView(generics.DestroyAPIView):
    """
    Given uuid and community id, removes the user from
    the community.
    """
    queryset = Community_members.objects.all()
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter = {"community" : self.kwargs["community"],
                  "member" : self.kwargs["member"]}
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        updateRecommendations(kwargs["member"], kwargs["community"], -1)
        return response

class EditCommunitySocialView(generics.RetrieveUpdateAPIView):
    """
    Edits the community socials if requested by admin
    """
    queryset = Communities.objects.all()
    serializer_class = CommunitiesCreateSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        membership_queryset = Community_members.objects.all()
        filter = {}
        membership_filter = {}
        membership_filter["community"] = self.kwargs["community"]
        membership_filter["member"] = self.kwargs["admin"]
        admin_obj = get_object_or_404(membership_queryset, **membership_filter)
        if admin_obj.admin:  
            obj = get_object_or_404(queryset, **filter)
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404("User is not an admin")

def updateRecommendations(user, community, change):
    """
    Function to update recommendations when a user joins or leaves a commmunity
    """
    membership_queryset = Community_members.objects.filter(ucid=community).exclude(member_id=user)
    for e in membership_queryset:
        recommendation = Recommendations.objects.get(user=user, recommendation=e.member_id)
        recommendation.similarity += change
        recommendation.save()
        recommendation = Recommendations.objects.get(user=e.member_id, recommendation=user)
        recommendation.similarity += change
        recommendation.save()