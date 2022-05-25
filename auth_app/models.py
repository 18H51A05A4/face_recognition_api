from unittest import defaultTestLoader
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.



# custom user model with usermanager
class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError('user must have a password')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_student(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',False)
        extra_fields.setdefault('is_teacher',False)
        return self.create_user(email,password,**extra_fields)

    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_teacher',True)
        return self.create_user(email,password,**extra_fields)
        


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255,unique = True)
    email = models.EmailField(max_length=255,unique = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
    
    LUDT = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = []

    # def get_full_name(self):
    #     return self.username 

    # def get_short_name(self):
    #     return self.username

    objects = UserManager()


    def __str__(self):
        return self.email
    


