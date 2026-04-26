from rest_framework import serializers
from .models import Airport, Flight, FlightSearch


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'iata_code', 'name', 'city', 'country']


class FlightSerializer(serializers.ModelSerializer):
    origin = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    origin_iata = serializers.CharField(write_only=True)
    destination_iata = serializers.CharField(write_only=True)

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'origin', 'destination', 'origin_iata', 'destination_iata',
                  'departure_time', 'arrival_time', 'price', 'currency', 'available_seats', 
                  'created_at', 'updated_at']

    def create(self, validated_data):
        origin_iata = validated_data.pop('origin_iata')
        destination_iata = validated_data.pop('destination_iata')
        
        origin, _ = Airport.objects.get_or_create(iata_code=origin_iata)
        destination, _ = Airport.objects.get_or_create(iata_code=destination_iata)
        
        validated_data['origin'] = origin
        validated_data['destination'] = destination
        
        return super().create(validated_data)


class FlightSearchSerializer(serializers.ModelSerializer):
    origin = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)
    origin_iata = serializers.CharField(write_only=True)
    destination_iata = serializers.CharField(write_only=True)

    class Meta:
        model = FlightSearch
        fields = ['id', 'origin', 'destination', 'origin_iata', 'destination_iata',
                  'departure_date_from', 'departure_date_to', 'return_date_from', 
                  'return_date_to', 'passengers', 'created_at']

    def create(self, validated_data):
        origin_iata = validated_data.pop('origin_iata')
        destination_iata = validated_data.pop('destination_iata')
        
        origin, _ = Airport.objects.get_or_create(iata_code=origin_iata)
        destination, _ = Airport.objects.get_or_create(iata_code=destination_iata)
        
        validated_data['origin'] = origin
        validated_data['destination'] = destination
        
        return super().create(validated_data)


class RyanairFlightSerializer(serializers.Serializer):
    flight_number = serializers.CharField()
    origin = serializers.CharField()
    destination = serializers.CharField()
    departure_time = serializers.CharField()
    arrival_time = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    available_seats = serializers.IntegerField()
    date = serializers.DateField()


class FlightSearchRequestSerializer(serializers.Serializer):
    origin_iata = serializers.CharField(max_length=3)
    destination_iata = serializers.CharField(max_length=3, required=False, allow_blank=True)
    departure_date_from = serializers.DateField()
    departure_date_to = serializers.DateField()
    return_date_from = serializers.DateField(required=False, allow_null=True)
    return_date_to = serializers.DateField(required=False, allow_null=True)
    passengers = serializers.IntegerField(min_value=1, max_value=9, default=1)
