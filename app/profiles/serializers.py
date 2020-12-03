from rest_framework import serializers
from .models import *


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('uuid', 'profile_visibility', 'follower_visibility',
        'following_visibility')

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_following
        fields = ('follower', 'following')

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_members
        fields = ('ucid', 'member_id', 'admin')

class CommunitySocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community_socials
        fields = ('ucid', 'discord', 'facebook', 'instagram')

class UserSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_socials
        fields = ('uuid', 'discord', 'facebook', 'snapchat',
         'github', 'linkedin', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    settings = SettingsSerializer
    communities = CommunityMemberSerializer
    socials = UserSocialSerializer
    class Meta:
        model = Profiles
        fields = ('uuid', 'first_name', 'last_name', 'major',
         'grad_year', 'profile_pic', 'settings', 'communities', 'socials')

class CommunitiesSerializer(serializers.ModelSerializer):
    members = CommunityMemberSerializer
    socials = CommunitySocialSerializer
    class Meta:
        model = Communities
        fields = ('ucid', 'title', 'description', 'profile_image_link',
         'active', 'members', 'socials')