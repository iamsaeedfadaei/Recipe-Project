from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,\
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    #password is none because we can have some user without password
    def create_user(self, email, password=None, **extra_fields):
        """creating and saving new user"""
        if not email:
            raise ValueError('Users must have an Email Address!')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)    # we use this function because passowrd is encrypted and cant be like email.
        user.save(using = self._db)      #we use using for maybe we use multiple db.
        
        return user


    def create_superuser(self, email, password):
        """creating and saving new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email insteadof username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag to be used for recipe."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name