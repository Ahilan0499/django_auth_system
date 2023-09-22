from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from shortuuidfield import ShortUUIDField
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator





class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**kwargs):

        """
        Creates and saves a new superuser with the given email and password.
        """
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_phone_verified=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user




class User(AbstractBaseUser,PermissionsMixin):
     
     ROLE_CHOICES = (
        ("admin", "admin"),
        ("client", "client"),
        ("user", "user"),
    )
     
     PASSOWRD_REGEX = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
     PASSWORD_VALIDTOR = RegexValidator(
        PASSOWRD_REGEX,
        "Password must be at min 8 char, one Uppercase, one lowercase, one number, one special character."
    )
     PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")



     app_id = ShortUUIDField()
     name=models.CharField(max_length=100,null=False,blank=False)
     email=models.EmailField(unique=True)
     password=models.CharField(max_length=255,validators=[PASSWORD_VALIDTOR])
     phonenumber = models.CharField(validators=[PHONE_REGEX],max_length=15,unique=True)
     role = models.CharField(choices=ROLE_CHOICES, blank=False, null=False,max_length=50)
     is_phone_verified = models.BooleanField(default=False)
     is_active = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
     updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
     is_staff = models.BooleanField(default=True)




     USERNAME_FIELD='email'
     REQUIRED_FIELDS=['phonenumber','role']

     objects = CustomUserManager()

     

     def __str__(self):
       return self.email

     class Meta:
       db_table = "user"
    




# Create your models here.
