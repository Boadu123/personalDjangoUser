from django.db import models
from user.models import CustomUser


# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    about_product = models.TextField()
    image = models.ImageField(upload_to='product_pics/', null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)