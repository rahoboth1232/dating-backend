from django.db import models
from django.contrib.auth.models import User
class Swipe(models.Model):
    swiper = models.ForeignKey(User, related_name='swipes_made', on_delete=models.CASCADE)
    swiped = models.ForeignKey(User, related_name='swipes_received', on_delete=models.CASCADE)
    liked = models.BooleanField()  # True = like, False = dislike
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('swiper', 'swiped')  # One swipe per user pair
class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='matches1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='matches2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user1', 'user2')
