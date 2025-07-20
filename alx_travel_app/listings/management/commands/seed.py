from django.core.management.base import BaseCommand
from listings.models import User, Location, Listing, Booking, Review
from django.utils import timezone
from decimal import Decimal
import datetime

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
            {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
            {"first_name": "Alice", "last_name": "Johnson", "email": "alice@example.com"},
        ]
        for user_data in users:
            User.objects.get_or_create(**user_data)
        self.stdout.write("Created users")

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
        users = User.objects.all()
        locations = Location.objects.all()
        
        listings = [
            {
                "host_id": users[0],
                "name": "Cozy Apartment",
                "description": "Beautiful apartment in city center",
                "location_id": locations[0],
                "price_per_night": Decimal("99.99")
            },
            {
                "host_id": users[1],
                "name": "Beach Villa",
                "description": "Luxury villa with ocean view",
                "location_id": locations[1],
                "price_per_night": Decimal("249.99")
            },
            {
                "host_id": users[2],
                "name": "Downtown Loft",
                "description": "Modern loft near financial district",
                "location_id": locations[2],
                "price_per_night": Decimal("149.99")
            },
        ]
        for listing_data in listings:
            Listing.objects.get_or_create(**listing_data)
        self.stdout.write("Created listings")

    def _create_bookings(self):
        listings = Listing.objects.all()
        users = User.objects.all()
        
        bookings = [
            {
                "host_id": users[0],
                "property_id": listings[0],
                "start_date": timezone.now().date(),
                "end_date": timezone.now().date() + datetime.timedelta(days=7),
                "total_price": listings[0].price_per_night * 7,
                "status": Booking.StatusChoices.CONFIRMED
            },
            {
                "host_id": users[1],
                "property_id": listings[1],
                "start_date": timezone.now().date() + datetime.timedelta(days=10),
                "end_date": timezone.now().date() + datetime.timedelta(days=17),
                "total_price": listings[1].price_per_night * 7,
                "status": Booking.StatusChoices.PENDING
            },
        ]
        for booking_data in bookings:
            Booking.objects.get_or_create(**booking_data)
        self.stdout.write("Created bookings")

    def _create_reviews(self):
        listings = Listing.objects.all()
        users = User.objects.all()
        
        reviews = [
            {
                "property_id": listings[0],
                "user_id": users[1],
                "rating": 5,
                "comment": "Perfect stay, highly recommend!"
            },
            {
                "property_id": listings[1],
                "user_id": users[2],
                "rating": 4,
                "comment": "Great location but a bit noisy"
            },
        ]
        for review_data in reviews:
            Review.objects.get_or_create(**review_data)
        self.stdout.write("Created reviews")