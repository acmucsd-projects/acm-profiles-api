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



