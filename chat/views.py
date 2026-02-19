from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from matches.models import Match
from rest_framework.exceptions import PermissionDenied

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        match = Match.objects.get(id=match_id)
        user = self.request.user
        # Ensure user is part of this match
        if match.user1 != user and match.user2 != user:
            raise PermissionDenied("You are not part of this match")
        return Message.objects.filter(match=match)

    def perform_create(self, serializer):
        match_id = self.kwargs['match_id']
        match = Match.objects.get(id=match_id)
        user = self.request.user
        # Ensure user is part of this match
        if match.user1 != user and match.user2 != user:
            raise PermissionDenied("You are not part of this match")
        serializer.save(sender=user, match=match)
