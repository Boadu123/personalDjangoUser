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
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

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

        user_data = CustomUserSerializer(user).data
        user_data.pop('password', None)

        return Response({
            "status": "201",
            "message": "You have Registered Successfully",
            'refresh': str(refresh),
            'access': str(access_token),
            'user': user_data,
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

        user_data = CustomUserSerializer(user).data
        user_data.pop('password', None)

        return Response({
            "status": "200",
            "message": "You have successfully Logged In",
            'refresh': str(refresh),
            'access': str(access_token),
            'user': user_data
        }, status=status.HTTP_200_OK)

    return Response({'detail':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = CustomUser.objects.all()
    if users:
        serializer = CustomUserSerializer(users, many=True)

        for user_data in serializer.data:
            user_data.pop('password', None)

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

    user_data = CustomUserSerializer(user).data
    user_data.pop('password', None)

    return Response({

        "status": "200",
        "message": "Users retrieved successfully",
        'users': user_data
}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    data = request.data.copy()  # duplicate the original data
    data.pop('email', None) # Remove email if available
    data.pop('password', None) # Remove password if available
    
    serializer = CustomUserSerializer(user, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

        user_data = serializer.data
        user_data.pop('password', None)

        return Response({
            "status": "200",
            "message": "User details updated successfully",
            "user": user_data
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

    data = request.data.copy()  # duplicate the original data
    data.pop('email', None) # Remove email if available
    data.pop('password', None) # Remove password if available
    
    serializer = CustomUserSerializer(user, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

        user_data = serializer.data
        user_data.pop('password', None)

        return Response({
            "status": "200",
            "message": "User details updated successfully",
            "user": user_data
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


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to log out
@authentication_classes([])  # No authentication needed since we're handling token revocation
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')  # Get the refresh token from the request
        
        if not refresh_token:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to decode and revoke the token
        token = RefreshToken(refresh_token)
        token.blacklist()  # Blacklisting the token ensures it cannot be used again
        
        return Response({
            "status": "200",
            "message": "You have successfully logged out"
        }, status=status.HTTP_200_OK)

    except InvalidToken:
        return Response({'detail': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_email(request):
    user = request.user
    new_email = request.data.get("email")

    if not new_email:
        raise ValidationError("Email field is required")
    
    if new_email == user.email:
        return Response({
            "status": "400",
            "message": "New email cannot be the same as the current email."
        }, status=status.HTTP_400_BAD_REQUEST)
    user.email = new_email
    user.save()

    user_data = CustomUserSerializer(user).data
    user_data.pop("password")

    return Response({
        "status": "200",
        "message": "Email updated successfully",
        "user": user_data
    }, status=status.HTTP_200_OK)  


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password:
        raise ValidationError("Old password is required.")
    
    if not new_password:
        raise ValidationError("New password is required.")
    
    # Check if the old password is correct
    if not check_password(old_password, user.password):
        return Response({
            "status": "400",
            "message": "Old password is incorrect."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Validate the new password using Django's password validators
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({
            "status": "400",
            "message": "Password validation error",
            "errors": e.messages
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update the password and save the user
    user.set_password(new_password)
    user.save()

    user_data = CustomUserSerializer(user).data
    user_data.pop("password")

    return Response({
        "status": "200",
        "message": "Password updated successfully",
        "user": user_data
    }, status=status.HTTP_200_OK)