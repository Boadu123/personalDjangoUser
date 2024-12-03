from django.urls import path
from .views import SignupView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]