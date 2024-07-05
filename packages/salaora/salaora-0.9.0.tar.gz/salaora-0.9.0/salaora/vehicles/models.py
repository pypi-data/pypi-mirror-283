from io import StringIO
import csv

from django.db import models

from salaora import now

class Vehicle(models.Model):
    COLOR_CHOICES = [
        ("Blue", "Blue"),
        ("Black", "Black"),
        ("White", "White"),
        ("Gray", "Gray")
    ]
    VEHICLE_TYPE_CHOICES = [
        ("Car", "Car"),
        ("Jeep", "Jeep"),
        ("ATV", "ATV"),
        ("Scooter", "Scooter")
    ]
    ENGINE_TYPE_CHOICES = [
        ("Gas", "Gas"),
        ("Diesel", "Diesel")
    ]

    @property
    def is_available(self, from_dt=None, to_dt=None):
        for reservation in self.reservation_set.all():
            if reservation.departure_dt < now < reservation.return_dt:
                return False
        return True

    model = models.CharField(max_length=100)
    plate = models.CharField(max_length=12, primary_key=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    engine_type = models.CharField(max_length=10, choices=ENGINE_TYPE_CHOICES)
    price = models.FloatField(blank=True)
    details = models.TextField(blank=True)
    image = models.FileField(upload_to="vehicle_images/", blank=True, default="defaults/no_car.png")
    license_image = models.FileField(upload_to="vehicle_images/license", blank=True, default="defaults/no_license.jpeg")
    insurance_pdf = models.FileField(upload_to="vehicle_insurances/", blank=True, default="defaults/no_document.pdf")


def populate_vehicles_from_csv_string(csv_data):
    f = StringIO(csv_data)
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        print(row)
        try:
            model = row[0]
            plate = row[1]
            color = row[2]
            vehicle_type = row[3]
            engine_type = row[4]
            price = float(row[5])
            details = row[6]

            vehicle = Vehicle(
                model = model,
                plate = plate,
                color = color,
                vehicle_type = vehicle_type,
                engine_type = engine_type,
                price = price,
                details = details
            )
            vehicle.full_clean()
            vehicle.save()
        except Exception as e:
            print(e)
