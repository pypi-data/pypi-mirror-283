from django.db import models

from vehicles.models import Vehicle

class Reservation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    departure_dt = models.DateTimeField()
    return_dt = models.DateTimeField()
    details = models.TextField(blank=True)
