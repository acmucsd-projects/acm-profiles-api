from django.db import models
import uuid

# Create your models here.

class Profiles(models.Model):
    uuid = models.CharField(primary_key = True, max_length = 255, unique = True)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    major = models.CharField(max_length = 255, blank = True)
    grad_year = models.IntegerField(blank = True)
    profile_pic = models.CharField(blank = True, null = True, max_length = 255)

class Settings(models.Model):
    uuid = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='settings')
    profile_visibility = models.BooleanField(default = True)
    follower_visibility = models.BooleanField(default = True)
    following_visibility = models.BooleanField(default = True)

class User_following(models.Model):
    follower = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='follower')

class Communities(models.Model):
    ucid = models.UUIDField(primary_key = True, default = uuid.uuid4, unique = True, editable = False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    profile_image_link = models.CharField(max_length=255, blank = True)
    active = models.BooleanField(max_length=255, default = True)

class Community_members(models.Model):
    ucid = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='members')
    member_id = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='communities')
    admin = models.BooleanField(default = False)

class Community_socials(models.Model):
    ucid = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='socials')
    discord = models.CharField(max_length=255, blank = True)
    facebook = models.CharField(max_length=255, blank = True)
    instagram = models.CharField(max_length=255, blank = True)

class User_socials(models.Model):
    uuid = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='socials')
    discord = models.CharField(max_length=255, blank = True)
    facebook = models.CharField(max_length=255, blank = True)
    snapchat = models.CharField(max_length=255, blank = True)
    github = models.CharField(max_length=255, blank = True)
    linkedin = models.CharField(max_length=255, blank = True)
    email = models.EmailField(blank = True)


