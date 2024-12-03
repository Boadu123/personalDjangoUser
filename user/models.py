from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
# Create your models here.

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email", max_length=40, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def set_password(self, password):
        self.password = make_password(password)