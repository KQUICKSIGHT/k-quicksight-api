# from django.db import models
# import uuid

# from django.contrib.auth.models import BaseUserManager

# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
# from django.db import models
# from django.utils import timezone
# from django.db import models
# from django.utils import timezone
# from datetime import timedelta

# def get_expiry_time():
#     return timezone.now() + timedelta(minutes=5)

# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("You have not provided a valid e-mail address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
    
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
#     username = models.CharField(max_length=20, unique=True)
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other')
#     ]
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
#     dob = models.DateField(verbose_name='Date of Birth',null=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)  # Use Django's built-in password handling instead.
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     biography = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     logged_in_at = models.DateTimeField(null=True, blank=True)
#     verification_code = models.CharField(max_length=6, null=True, blank=True)
#     expired_at = models.DateTimeField(default=get_expiry_time)
#     is_deleted = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)
#     objects = CustomUserManager()


#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
    
#     def get_full_name(self):
#         return self.username
    
#     def get_short_name(self):
#         return self.username or self.email.split('@')[0]
    
#     @property
#     def is_anonymous(self):
#         return False

#     @property
#     def is_authenticated(self):
#         return True


