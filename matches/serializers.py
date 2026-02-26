from rest_framework import serializers
from .models import Swipe, Match, Message

class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = ['swiped', 'liked']

class MatchSerializer(serializers.ModelSerializer):
    user1 = serializers.CharField(source='user1.username', read_only=True)
    user2 = serializers.CharField(source='user2.username', read_only=True)
    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'timestamp']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = Message
        fields = ['sender', 'content', 'timestamp']
