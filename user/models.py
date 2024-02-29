from django.db import models
import uuid

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone
from datetime import timedelta


def get_expiry_time():
    return timezone.now() + timedelta(minutes=5)


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        email = self.normalize_email(email)

        existing_user = User.objects.filter(email=email, is_deleted=False).first()
        if existing_user:
            raise ValueError("A user with this email already exists")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email',"github": 'github'}


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(verbose_name='Date of Birth', null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    avatar = models.CharField(null=True, blank=True)
    storage_data = models.FloatField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    logged_in_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    uid_base64= models.CharField(max_length=255, blank=True, null=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    expired_at = models.DateTimeField(default=get_expiry_time, null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = "users"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username or self.email.split('@')[0]

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




# Create a UserRole model to establish the relationship between User and Role
