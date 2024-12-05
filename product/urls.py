from django.urls import path
from .views import add_Product

urlpatterns = [
        path('product/', add_Product, name='add_Product')
]