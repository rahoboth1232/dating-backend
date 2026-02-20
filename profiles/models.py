from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=20,
        choices=[('Male','Male'),('Female','Female'),('Other','Other')],
        blank=True
    )   
    interested_in = models.CharField(max_length=20)
    interests = models.JSONField(default=list, blank=True)
    photo = models.ImageField(upload_to="profile_photos/")

    def __str__(self):
        return self.user.email


 