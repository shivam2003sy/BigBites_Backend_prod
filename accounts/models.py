from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user_type = extra_fields.pop('user_type', 'admin')
        if extra_fields.get('is_staff') is False:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, user_type='admin', **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = None
    firebase_uid = models.CharField(max_length=255, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Customer(User):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    profile_image_url = models.URLField(blank=True, null=True)
    push_notification_token = models.CharField(max_length=255, blank=True, null=True)
    account_created_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    location_last_updated = models.DateTimeField(blank=True, null=True)

class Restaurant(User):

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=100, blank=True, null=True)
    subscription_expiry_date = models.DateTimeField(blank=True, null=True)
    operating_hours = models.JSONField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    kitchen_type = models.JSONField(blank=True, null=True)
    is_priority_listing = models.BooleanField(default=False)
    menu_categories = models.JSONField(blank=True, null=True)
    localized_categories = models.JSONField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    varified_restaurant = models.OneToOneField('RestaurantVerified', on_delete=models.CASCADE, blank=True, null=True)
  


class RestaurantVerified(models.Model):
    status  = {
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('initiated', 'Initiated'),
    }
    status = models.CharField(max_length=50, choices=status, default='initiated')
    verification_date = models.DateTimeField(auto_now_add=True)
    verification_notes = models.TextField(blank=True, null=True)




    