from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin,Group, Permission
from rest_framework.authtoken.models import Token
import binascii
import os
from django.conf import settings

# Create your models here.     

class UserToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    # Ensure a unique related_name to avoid conflicts
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_token',  # Ensure this is unique
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self._generate_key()
        super().save(*args, **kwargs)

    def _generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

# Product
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    unit_price = models.DecimalField(max_digits= 6 , decimal_places= 2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


# Customer
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name='customers', blank=True)  # Change related_name to avoid clash
    user_permissions = models.ManyToManyField(Permission, related_name='customers', blank=True)  # Change related_name to avoid clash

    def __str__(self):
        return self.email

# Order
class Order (models.Model): 
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING , 'Pending'),
        (PAYMENT_COMPLETE , 'Complete'),
        (PAYMENT_FAILED   , 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length= 1 , choices=PAYMENT_STATUS_CHOICES , default=PAYMENT_PENDING)
    customer =  models.ForeignKey(Customer, on_delete=models.PROTECT )

# OrderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

# Address
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length= 255,null=True)
