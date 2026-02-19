from django.shortcuts import render
from rest_framework import generics
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        # Check if 'user' and 'password' are provided in the request
        username = request.data.get("user")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate token using Simple JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return success response with access token and user info
            return Response({
                "message": "Login successful",
                "user": {"username": user.username},
                "token": access_token,
            })
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  
