from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup_view(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()

        subject = 'Welcome to Our Website!'
        message = f'Hello {user.first_name} {user.last_name}, thank you for registering on our website.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list)

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
    
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = CustomUser.objects.filter(email=email).first()

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

    return Response({'detail':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = CustomUser.objects.all()
    if users:
        serializer = CustomUserSerializer(users, many=True)
        return Response({
            "status": "200",
            "message": "Users retrieved successfully",
            'users': serializer.data
        }, status=status.HTTP_200_OK)
    return Response({'detail': 'No users found'}, status=status.HTTP_404_NOT_FOUND)   


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):

    user = request.user
    
    serializer = CustomUserSerializer(user)
    return Response({

        "status": "200",
        "message": "Users retrieved successfully",
        'users': serializer.data
}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "200",
            "message": "User details updated successfully",
            "user": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        "status": "400",
        "message": "Failed to update user details",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_user(request):
    user = request.user
    
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "200",
            "message": "User details updated successfully",
            "user": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        "status": "400",
        "message": "Failed to update user details",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user

    subject = 'Attention! Deleting your account'
    message = f'Hello {user.first_name} {user.last_name}, your account has been deleted'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
    
    user.delete()

    return Response({
        "status": "200",
        "message": "User deleted successfully"
    }, status=status.HTTP_200_OK)
