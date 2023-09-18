from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)




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

    def create_superuser(self, email, password):
        """
        Creates and saves a new superuser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser,PermissionsMixin):
     
     ROLE_CHOICES = (
        ("admin", "admin"),
        ("client", "client"),
        ("consultant", "consultant"),
    )
     username=None

     
     name=models.CharField(max_length=100,null=False,blank=False)
     email=models.EmailField(unique=True)
     password=models.CharField(max_length=255)
     phonenumber = models.CharField(max_length=15, null=True, blank=True)
     role = models.CharField(choices=ROLE_CHOICES, blank=False, null=False,max_length=50)
     is_active = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
     updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
     is_staff = models.BooleanField(default=False)
    



     USERNAME_FIELD='email'
     REQUIRED_FIELDS=[]

     objects = CustomUserManager()

     def __str__(self):
       return self.email

     class Meta:
       db_table = "user"
    




# Create your models here.
