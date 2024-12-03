from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status




# Create your views here.

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)