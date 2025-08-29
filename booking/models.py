from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class TravelOption(models.Model):
    FLIGHT = 'Flight'
    TRAIN = 'Train'
    BUS = 'Bus'

    TRAVEL_TYPE_CHOICES = [
        (FLIGHT, 'Flight'),
        (TRAIN, 'Train'),
        (BUS, 'Bus'),
    ]

    travel_type = models.CharField(
        max_length=10,
        choices=TRAVEL_TYPE_CHOICES,
        default=FLIGHT,
    )
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.travel_type} from {self.source} to {self.destination} on {self.datetime.strftime('%Y-%m-%d %H:%M')}"



class Booking(models.Model):
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey('TravelOption', on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CONFIRMED)

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username} - {self.status}"