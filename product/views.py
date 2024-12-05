from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status




# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save(user=request.user)
        product.save()
        return Response({
            "status": "201",
            "message": "You have added product Successfully",
            'product': ProductSerializer(product).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)