from django.urls import path
from .views import add_Product, get_products, get_user_products, get_user_product, delete_user_product, update_user_product, patch_user_product

urlpatterns = [
        path('product/', add_Product, name='add_Product'),
        path('products/', get_products, name='get_products'),
        path('user-products/', get_user_products, name='get_user_products'),
        path('user-product/<int:id>/', get_user_product, name='get_user_product'),
        path('delete-product/<int:id>/', delete_user_product, name='delete_user_product'),
        path('update-product/<int:id>/', update_user_product, name='update_user_product'),
        path('partial-update-product/<int:id>/', patch_user_product, name='patch_user_product')
]