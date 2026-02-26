from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from profiles.models import Profile
from .models import Swipe, Match, Message
from .serializers import SwipeSerializer, MatchSerializer, MessageSerializer


class SuggestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        my_profile = user.profile

        swiped_users = Swipe.objects.filter(
            swiper=user
        ).values_list('swiped_id', flat=True)

        suggestions = Profile.objects.exclude(
            Q(user=user) | Q(user__id__in=swiped_users)
        )

        suggestions = suggestions.filter(
            gender=my_profile.interested_in,
            interested_in=my_profile.gender
        )

        results = []

        for profile in suggestions:
            shared = list(
                set(my_profile.interests) & set(profile.interests)
            )

            results.append({
                "user_id": profile.user.id,
                "username": profile.user.username,
                "age": profile.age,
                "bio": profile.bio,
                "shared_interests": shared,
                "match_score": len(shared)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return Response(results)
    
class SwipeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        swiper = request.user
        swiped_id = request.data.get("swiped_id")
        liked = request.data.get("liked")

        if not swiped_id:
            return Response({"error": "swiped_id required"}, status=400)

        if int(swiped_id) == swiper.id:
            return Response({"error": "Cannot swipe yourself"}, status=400)

        try:
            swiped_user = User.objects.get(id=swiped_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        Swipe.objects.update_or_create(
            swiper=swiper,
            swiped=swiped_user,
            defaults={'liked': liked}
        )

        # Check mutual like
        if liked:
            mutual = Swipe.objects.filter(
                swiper=swiped_user,
                swiped=swiper,
                liked=True
            ).exists()

            if mutual:
                user1, user2 = sorted([swiper, swiped_user], key=lambda u: u.id)

                match, created = Match.objects.get_or_create(
                    user1=user1,
                    user2=user2
                )

                if created:
                    return Response({"message": "It's a Match ❤️"}, status=201)

        return Response({"message": "Swipe recorded"}, status=201)
    
class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(Q(user1=user) | Q(user2=user))
class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, match_id):
        user = request.user
        content = request.data.get("content")

        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return Response({"error": "Match not found"}, status=404)

        if user != match.user1 and user != match.user2:
            return Response({"error": "Not allowed"}, status=403)

        Message.objects.create(
            match=match,
            sender=user,
            content=content
        )

        return Response({"message": "Message sent"})
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        user = self.request.user

        match = Match.objects.get(id=match_id)

        if user != match.user1 and user != match.user2:
            return Message.objects.none()

        return Message.objects.filter(match=match).order_by('timestamp')