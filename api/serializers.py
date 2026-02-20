from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid username or password")
from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    email= serializers.EmailField(required=True)
    bio = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.CharField()
    interested_in = serializers.CharField()
    interests = serializers.ListField(child=serializers.CharField())
    photo = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'confirm_password',
            'bio',
            'age',
            'gender',
            'interested_in',
            'interests',
            'photo'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'photo': {'required': True}
        }


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from validated_data
        bio = validated_data.pop('bio')
        age = validated_data.pop('age')
        gender = validated_data.pop('gender')
        interested_in = validated_data.pop('interested_in')
        interests = validated_data.pop('interests')
        photo = validated_data.pop('photo')

        user = User.objects.create_user(**validated_data)

        Profile.objects.create(
            user=user,
            bio=bio,
            age=age,
            gender=gender,
            interested_in=interested_in,
            interests=interests,
            photo=photo
        )
        return user
