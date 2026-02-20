from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from django.views.decorators.csrf import csrf_exempt


from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
