from django.db import models
from django.utils import timezone


class Airport(models.Model):
    iata_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.iata_code} - {self.name}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    available_seats = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flight_number}: {self.origin.iata_code} -> {self.destination.iata_code} ({self.price} {self.currency})"


class FlightSearch(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='searches_from')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='searches_to')
    departure_date_from = models.DateField()
    departure_date_to = models.DateField()
    return_date_from = models.DateField(null=True, blank=True)
    return_date_to = models.DateField(null=True, blank=True)
    passengers = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search: {self.origin.iata_code} -> {self.destination.iata_code}"
