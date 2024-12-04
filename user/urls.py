from django.urls import path
from .views import signup_view, login_view, get_users, get_user


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('users/', get_users, name='users'),
    path('', get_user, name='users')
]