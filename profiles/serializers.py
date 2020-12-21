from rest_framework import serializers
from .models import *


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('user', 'profile_visibility', 'follower_visibility',
        'following_visibility')

class FollowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_following
        fields = ('follower',)

class FollowingListSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User_following
        fields = ('following',)

class FollowingEmptySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_following
        fields = ()

class CommunityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_members
        fields = ('community',)

class MemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_members
        fields = ('member', 'admin')

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_members
        fields = ('community', 'member', 'admin')

class JoinCommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_members
        fields = ()

class CommunitySocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_socials
        fields = ('community', 'discord', 'facebook', 'instagram')

class UserSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socials
        fields = ('user', 'discord', 'facebook', 'snapchat',
         'github', 'linkedin', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ('uuid', 'first_name', 'last_name', 'major', 
        'grad_year', 'college', 'profile_pic', 'bio')

class CommunitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communities
        fields = ('ucid', 'title', 'description', 'profile_image_link',
         'active')

class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = ('recommendation',)