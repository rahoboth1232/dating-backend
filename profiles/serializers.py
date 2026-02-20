from rest_framework import serializers
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'age',
            'gender',
            'interested_in',
            'interests',
            'photo'
        ]
