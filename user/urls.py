from django.urls import path
from .views import signup_view, login_view, get_users, get_user, update_user, patch_user, delete_user, logout_view, change_email, change_password


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('users/', get_users, name='users'),
    path('user/', get_user, name='user'),
    path('update/', update_user, name='update'),
    path('patch/', patch_user, name='patch'),
    path('delete/', delete_user, name='delete'),
    path('logout/', logout_view, name='logout'),
    path('change_email/', change_email, name='change_email'),
    path('change_password/', change_password, name='change_password'),
]