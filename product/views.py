from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_Product(request):
    # Initialize the serializer with the request data
    serializer = ProductSerializer(data=request.data)

    # Check if the data provided is valid
    if serializer.is_valid():
        # Save the product with the logged-in user as the owner
        product = serializer.save(user=request.user)

        return Response({
            "status": "201",
            "message": "Product added successfully",
            "product": ProductSerializer(product).data
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "400",
        "message": "Invalid data",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(request):
    # Retrieve all products
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)
    
    return Response({
        "status": "200",
        "message": "Products retrieved successfully",
        "products": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_products(request):
    # Retrieve all products for the logged-in user
    products = Product.objects.filter(user=request.user)

    if not products:
        return Response({
            "status": "404",
            "message": "No products found for this user"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(products, many=True)

    return Response({
        "status": "200",
        "message": "Products retrieved successfully",
        "products": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_product(request, id):
    try:
        # Retrieve the product for the logged-in user by its 'id'
        product = Product.objects.get(id=id, user=request.user)
    except Product.DoesNotExist:
        return Response({
            "status": "404",
            "message": "Product not found or does not belong to this user"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)

    return Response({
        "status": "200",
        "message": "Product retrieved successfully",
        "product": serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_product(request, id):
    try:
        # Retrieve the product for the logged-in user by its 'id'
        product = Product.objects.get(id=id, user=request.user)
    except Product.DoesNotExist:
        return Response({
            "status": "404",
            "message": "Product not found or does not belong to this user"
        }, status=status.HTTP_404_NOT_FOUND)

    product.delete()

    return Response({
        "status": "200",
        "message": "Product deleted successfully"
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_product(request, id):
    try:
        # Retrieve the product for the logged-in user by its 'id'
        product = Product.objects.get(id=id, user=request.user)
    except Product.DoesNotExist:
        return Response({
            "status": "404",
            "message": "Product not found or does not belong to this user"
        }, status=status.HTTP_404_NOT_FOUND)

    # Deserialize the request data and update the product instance
    serializer = ProductSerializer(product, data=request.data, partial=False)  # Use `partial=True` for partial updates

    if serializer.is_valid():
        serializer.save()  # Save the updated product
        return Response({
            "status": "200",
            "message": "Product updated successfully",
            "product": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_user_product(request, id):
    try:
        # Retrieve the product for the logged-in user by its 'id'
        product = Product.objects.get(id=id, user=request.user)
    except Product.DoesNotExist:
        return Response({
            "status": "404",
            "message": "Product not found or does not belong to this user"
        }, status=status.HTTP_404_NOT_FOUND)

    # Deserialize the request data and update the product instance with partial=True
    serializer = ProductSerializer(product, data=request.data, partial=True)  # Use `partial=True` for partial updates

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "200",
            "message": "Product updated successfully",
            "product": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
