# Generated by Django 3.1.3 on 2020-12-11 03:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communities',
            fields=[
                ('ucid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('profile_image_link', models.CharField(blank=True, max_length=255)),
                ('active', models.BooleanField(default=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('major', models.CharField(blank=True, max_length=255)),
                ('grad_year', models.IntegerField(blank=True, null=True)),
                ('profile_pic', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_socials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord', models.CharField(blank=True, max_length=255)),
                ('facebook', models.CharField(blank=True, max_length=255)),
                ('snapchat', models.CharField(blank=True, max_length=255)),
                ('github', models.CharField(blank=True, max_length=255)),
                ('linkedin', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socials', to='profiles.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='User_following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='profiles.profiles')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='profiles.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_visibility', models.BooleanField(default=True)),
                ('follower_visibility', models.BooleanField(default=True)),
                ('following_visibility', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='profiles.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity', models.IntegerField(default=0)),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_user', to='profiles.profiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='profiles.profiles')),
            ],
        ),
        migrations.CreateModel(
            name='Community_socials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord', models.CharField(blank=True, max_length=255)),
                ('facebook', models.CharField(blank=True, max_length=255)),
                ('instagram', models.CharField(blank=True, max_length=255)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socials', to='profiles.communities')),
            ],
        ),
        migrations.CreateModel(
            name='Community_members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='profiles.communities')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities', to='profiles.profiles')),
            ],
        ),
    ]
