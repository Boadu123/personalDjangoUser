from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'about_product', 'image', 'created', 'updated']
        read_only_fields = ['created', 'updated']