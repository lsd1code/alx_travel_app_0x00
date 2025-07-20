from rest_framework import serializers
from .models import Listing, Booking


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ListingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True)
    city = serializers.CharField(source='location_id.city')
    country = serializers.CharField(source='location_id.country')
    zip_code = serializers.CharField(source='location_id.zip_code')

    class Meta:
        model = Listing
        fields = [
            'property_id',
            'host_id',
            'name',
            'city',
            'country',
            'zip_code',
            'price_per_night',
            'created_at'
        ]
