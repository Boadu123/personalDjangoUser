from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password






# Create your views here.

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "status": "201",
                "message": "You have Registered Successfully",
                'refresh': str(refresh),
                'access': str(access_token),
                'user': CustomUserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()
        print(user.password)
        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "status": "200",
                "message": "You have successfully Logged In",
                'refresh': str(refresh),
                'access': str(access_token),
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    

# class GetallUsers(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):


