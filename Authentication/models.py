from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('publisher', 'Publisher'),
    )

    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    password = models.CharField(max_length=128, blank=False)
    # reset_password_token = models.CharField(max_length=255, blank=True)
    # reset_password_expire = models.DateTimeField(null=True, blank=True)
    # confirm_email_token = models.CharField(max_length=255, blank=True)
    # is_email_confirmed = models.BooleanField(default=False)
    # two_factor_code = models.CharField(max_length=6, blank=True)
    # two_factor_code_expire = models.DateTimeField(null=True, blank=True)
    # two_factor_enable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  


    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    def __str__(self):
        return self.email