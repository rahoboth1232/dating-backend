from django.db import models
from django.contrib.auth.models import User
class Swipe(models.Model):
    swiper = models.ForeignKey(User, related_name="swipes_made", on_delete=models.CASCADE)
    swiped = models.ForeignKey(User, related_name="swipes_received", on_delete=models.CASCADE)
    liked = models.BooleanField()
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('swiper', 'swiped')
class Match(models.Model):
    user1 = models.ForeignKey(User, related_name="matches_as_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="matches_as_user2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user1', 'user2')
class Message(models.Model):
    match = models.ForeignKey(Match, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    