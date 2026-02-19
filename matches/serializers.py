from rest_framework import serializers
from .models import Swipe, Match
from django.contrib.auth.models import User

class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = ['swiper', 'swiped', 'liked', 'timestamp']

class MatchSerializer(serializers.ModelSerializer):
    user1 = serializers.CharField(source='user1.username', read_only=True)
    user2 = serializers.CharField(source='user2.username', read_only=True)

    class Meta:
        model = Match
        fields = ['user1', 'user2', 'timestamp']
