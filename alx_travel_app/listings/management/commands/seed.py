from django.core.management.base import BaseCommand
from listings.models import User, Location, Listing, Booking, Review
from django.utils import timezone
from decimal import Decimal
import datetime

import uuid

class Command(BaseCommand):
    help = 'Populates database with sample listings data'
    
    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")
        self._create_users()
        self._create_locations()
        self._create_listings()
        self._create_bookings()
        self._create_reviews()
        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))

    def _create_users(self):
        users = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password_hash": "pbkdf2_sha256$600000$fakehashabc123$...",  # Should be real hash in production
                "phone_number": "12345678901",
                "role": User.RoleChoices.HOST
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com",
                "password_hash": "pbkdf2_sha256$600000$fakehashdef456$...",
                "phone_number": "12345678902",
                "role": User.RoleChoices.GUEST
            },
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice@example.com",
                "password_hash": "pbkdf2_sha256$600000$fakehashghi789$...",
                "phone_number": "12345678903",
                "role": User.RoleChoices.ADMIN,
                "is_staff": True
            },
        ]
        
        for user_data in users:
            # Use get_or_create to avoid duplicates
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "password_hash": user_data["password_hash"],
                    "phone_number": user_data["phone_number"],
                    "role": user_data["role"],
                    "is_staff": user_data.get("is_staff", False),
                }
            )
            if created:
                self.stdout.write(f"Created user: {user.email}")
            else:
                self.stdout.write(f"User already exists: {user.email}")

    def _create_locations(self):
        locations = [
            {"city": "New York", "country": "USA", "zip_code": 10001},
            {"city": "Los Angeles", "country": "USA", "zip_code": 90001},
            {"city": "London", "country": "UK", "zip_code": 10001},
        ]
        for loc_data in locations:
            Location.objects.get_or_create(**loc_data)
        self.stdout.write("Created locations")

    def _create_listings(self):
        host = User.objects.get(email="john@example.com")
        admin = User.objects.get(email="alice@example.com")
        locations = Location.objects.all()
        
        listings = [
            {
                "host_id": host,
                "name": "Cozy Apartment",
                "description": "Beautiful apartment in city center",
                "location_id": locations[0],
                "price_per_night": Decimal("99.99")
            },
            {
                "host_id": admin,
                "name": "Beach Villa",
                "description": "Luxury villa with ocean view",
                "location_id": locations[1],
                "price_per_night": Decimal("249.99")
            },
            {
                "host_id": host,
                "name": "Downtown Loft",
                "description": "Modern loft near financial district",
                "location_id": locations[2],
                "price_per_night": Decimal("149.99")
            },
        ]
        for listing_data in listings:
            Listing.objects.get_or_create(
                name=listing_data["name"],
                defaults=listing_data
            )
        self.stdout.write("Created listings")

    def _create_bookings(self):
        guest = User.objects.get(email="jane@example.com")
        listings = Listing.objects.all()
        
        bookings = [
            {
                "host_id": listings[0].host_id,
                "property_id": listings[0],
                "start_date": timezone.now().date(),
                "end_date": timezone.now().date() + datetime.timedelta(days=7),
                "total_price": listings[0].price_per_night * 7,
                "status": Booking.StatusChoices.CONFIRMED
            },
            {
                "host_id": listings[1].host_id,
                "property_id": listings[1],
                "start_date": timezone.now().date() + datetime.timedelta(days=10),
                "end_date": timezone.now().date() + datetime.timedelta(days=17),
                "total_price": listings[1].price_per_night * 7,
                "status": Booking.StatusChoices.PENDING
            },
        ]
        for booking_data in bookings:
            Booking.objects.get_or_create(
                property_id=booking_data["property_id"],
                start_date=booking_data["start_date"],
                defaults=booking_data
            )
        self.stdout.write("Created bookings")

    def _create_reviews(self):
        guest = User.objects.get(email="jane@example.com")
        listings = Listing.objects.all()
        
        reviews = [
            {
                "property_id": listings[0],
                "user_id": guest,
                "rating": 5,
                "comment": "Perfect stay, highly recommend!"
            },
            {
                "property_id": listings[1],
                "user_id": guest,
                "rating": 4,
                "comment": "Great location but a bit noisy"
            },
        ]
        for review_data in reviews:
            Review.objects.get_or_create(
                property_id=review_data["property_id"],
                user_id=review_data["user_id"],
                defaults=review_data
            )
        self.stdout.write("Created reviews")