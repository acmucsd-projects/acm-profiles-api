from django.db import models
import uuid

# Create your models here.

class Profiles(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    major = models.CharField(max_length = 255, blank = True, null = True)
    grad_year = models.IntegerField(blank = True, null = True)
    college = models.CharField(max_length = 255, blank = True, null = True)
    profile_pic = models.CharField(max_length = 255, blank = True, null = True)
    bio = models.TextField(blank = True, null = True)

class Settings(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='settings')
    profile_visibility = models.BooleanField(default = True)
    follower_visibility = models.BooleanField(default = True)
    following_visibility = models.BooleanField(default = True)

class User_following(models.Model):
    follower = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='follower')

class Communities(models.Model):
    ucid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length=255, unique = True)
    description = models.TextField(blank = True, null = True)
    profile_image_link = models.CharField(max_length=255, blank = True, null = True)
    active = models.BooleanField(max_length=255, blank = True, default = True)

class Community_members(models.Model):
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='communities')
    admin = models.BooleanField(default = False)

class Community_socials(models.Model):
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='socials')
    discord = models.CharField(max_length=255, blank = True, null = True)
    facebook = models.CharField(max_length=255, blank = True, null = True)
    instagram = models.CharField(max_length=255, blank = True, null = True)

class User_socials(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='socials')
    discord = models.CharField(max_length=255, blank = True, null = True)
    facebook = models.CharField(max_length=255, blank = True, null = True)
    instagram = models.CharField(max_length=255, blank = True, null = True)
    snapchat = models.CharField(max_length=255, blank = True, null = True)
    github = models.CharField(max_length=255, blank = True, null = True)
    linkedin = models.CharField(max_length=255, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)

class Recommendations(models.Model):
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='recommendations')
    recommendation = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='recommended_user')
    similarity = models.IntegerField(default=0)


