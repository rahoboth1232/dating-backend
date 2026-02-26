from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    interested_in = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="profiles/", null=True, blank=True)
    interests = models.JSONField(default=list)

    def __str__(self):
        return self.user.username

 