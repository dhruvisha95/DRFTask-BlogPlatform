from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, verbose_name=("Full Name"))
    bio = models.TextField(blank=True, verbose_name=("Bio"))
    picture = models.ImageField(upload_to="profile_pictures/", blank=True, verbose_name=("Profile Picture"))
    phone_number = models.CharField(max_length=15, blank=True, verbose_name=("Phone Number"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name
