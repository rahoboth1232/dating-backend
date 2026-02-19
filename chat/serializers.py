from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'match', 'sender', 'sender_username', 'content', 'timestamp']
        read_only_fields = ['sender', 'timestamp']
