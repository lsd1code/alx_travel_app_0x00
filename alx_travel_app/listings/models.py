from django.db import models

import uuid

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)


class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    zip_code = models.PositiveIntegerField(blank=False)

    def __str__(self) -> str:
        return f'{self.country} {self.city} {self.zip_code}'


class Listing(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='listings')
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='listings')
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

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='host')
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=15, choices=StatusChoices, default=StatusChoices.PENDING)
    created_at = models.DateField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'Booking {self.booking_id}: '


class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return f'{self.review_id}: {self.rating} - {self.comment}'
