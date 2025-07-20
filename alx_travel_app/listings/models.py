from django.db import models
from django.contrib.auth.models import AbstractBaseUser

import uuid


class User(AbstractBaseUser):
    class RoleChoices(models.TextChoices):
        GUEST = "guest"
        HOST = "host"
        ADMIN = "admin"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    role = models.CharField(
        max_length=10, choices=RoleChoices, default=RoleChoices.GUEST)
    creates_at = models.DateField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return f'User {self.user_id}: {self.first_name.capitalize()} {self.last_name.capitalize()}'


class Location(models.Model):
    location_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    zip_code = models.PositiveIntegerField(blank=False)

    def __str__(self) -> str:
        return f'{self.country} {self.city} {self.zip_code}'


class Listing(models.Model):
    property_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='listings')
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    location_id = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='listings')
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateField(auto_now=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=True)

    def __str__(self) -> str:
        return f'{self.property_id} - R{self.price_per_night}'


class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"

    booking_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='host')
    property_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(
        max_length=15, choices=StatusChoices, default=StatusChoices.PENDING)
    created_at = models.DateField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'Booking {self.booking_id}: '


class Review(models.Model):
    review_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listings")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'{self.review_id}: {self.rating} - {self.comment}'
