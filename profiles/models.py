from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[('Male','Male'),('Female','Female'),('Other','Other')],
        blank=True
    )
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    preference_gender = models.CharField(
        max_length=20,
        choices=[('Male','Male'),('Female','Female'),('Both','Both')],
        default='Both'
    )
    def __str__(self):
        return self.user.username
