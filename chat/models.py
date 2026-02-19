from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from matches.models import Match

class Message(models.Model):
    match = models.ForeignKey(Match, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
