from django.db import models

# Create your models here.

class Profiles(models.Model):
    uuid = models.CharField(primary_key = True, max_length = 255, unique = True)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    major = models.CharField(max_length = 255)
    grad_year = models.IntegerField()
    profile_pic = models.CharField(blank = true, null = true, max_length = 255)

class Settings(models.Model):
    uuid = models.CharField(primary_key = True, max_length = 255, unique = True)
    profile_visibility = models.BooleanField(default = True)
    follower_visibility = models.BooleanField(default = True)
    following_visibility = models.BooleanField(default = True)

class User_Socials(models.Model):
    follower = models.CharField(max_length = 255)
    following = models.CharField(max_length = 255)

class Communities(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(s)
    profile_image_link = models.CharField()
    active = models.BooleanField(max_length=255)

class Community_members(models.Model):
    ucid = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='members')
    member_id = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='communities')
    admin = models.BooleanField()

class Community_socials(models.Model):
    ucid = models.ForeignKey(Communities, on_delete=models.CASCADE, related_name='socials')
    discord = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)

class User_socials(models.Model):
    uuid = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='communities')
    discord = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    snapchat = models.CharField(max_length=255)
    github = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


