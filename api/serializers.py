from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from profiles.models import Profile


# ------------------ LOGIN ------------------

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid username or password")


# ------------------ REGISTER ------------------
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from profiles.models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    bio = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    gender = serializers.CharField(write_only=True)
    interested_in = serializers.CharField(write_only=True)
    photo = serializers.ImageField(required=False, write_only=True)
    interests = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "bio",
            "age",
            "gender",
            "interested_in",
            "photo",
            "interests",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        bio = validated_data.pop("bio")
        age = validated_data.pop("age")
        gender = validated_data.pop("gender")
        interested_in = validated_data.pop("interested_in")
        photo = validated_data.pop("photo", None)
        interests = validated_data.pop("interests")

        user = User.objects.create_user(**validated_data)

        Profile.objects.create(
            user=user,
            bio=bio,
            age=age,
            gender=gender,
            interested_in=interested_in,
            photo=photo,
            interests=interests,
        )

        return user