from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    GENDER_CHOICES = [("MALE", 0), ("FEMALE", 1), ("OTHER", 2)]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    age = models.SmallIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bloodgroup = models.CharField(max_length=10)
    profile_pic = models.ImageField()