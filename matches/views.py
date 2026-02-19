from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Swipe, Match
from .serializers import SwipeSerializer, MatchSerializer
from django.contrib.auth.models import User


class SwipeView(generics.CreateAPIView):
    serializer_class = SwipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        swiped_id = request.data.get('swiped_id')
        liked = request.data.get('liked', True)
        swiper = request.user

        if swiped_id == swiper.id:
            return Response({"error": "Cannot swipe yourself"}, status=status.HTTP_400_BAD_REQUEST)

        swiped_user = User.objects.get(id=swiped_id)

        # Save swipe
        swipe, created = Swipe.objects.update_or_create(
            swiper=swiper,
            swiped=swiped_user,
            defaults={'liked': liked}
        )

        # Check if mutual like → create Match
        if liked:
            if Swipe.objects.filter(swiper=swiped_user, swiped=swiper, liked=True).exists():
                # Create match if not exists
                if not Match.objects.filter(
                    user1=min(swiper.id, swiped_user.id),
                    user2=max(swiper.id, swiped_user.id)
                ).exists():
                    Match.objects.create(
                        user1=User.objects.get(id=min(swiper.id, swiped_user.id)),
                        user2=User.objects.get(id=max(swiper.id, swiped_user.id))
                    )
                    return Response({"message": "It's a match!"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Swipe saved"}, status=status.HTTP_201_CREATED)

class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(models.Q(user1=user) | models.Q(user2=user))
