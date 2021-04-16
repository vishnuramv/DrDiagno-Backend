from rest_framework import serializers
from .models import Profile


class ProfileSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("username", "age", "gender", "profile_pic", "bloodgroup")