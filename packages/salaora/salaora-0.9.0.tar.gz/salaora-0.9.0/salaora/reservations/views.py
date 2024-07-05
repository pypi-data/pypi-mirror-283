from datetime import datetime, timedelta

from django.shortcuts import render
from django.shortcuts import redirect

from salaora import now_cleaned

from reservations.models import Reservation
from reservations.forms import ReservationForm

from vehicles.models import Vehicle

def crud_reservation(request, pk=0):

    if request.method == "POST":

        reservation = None
        form = ReservationForm(request.POST)
        vehicle = Vehicle.objects.get(pk=form["vehicle"].value())
        client_name = form["client_name"].value()
        departure_dt = form["departure_dt"].value()
        return_dt = form["return_dt"].value()
        details = form["details"].value()

        if pk:
            try:
                reservation = Reservation.objects.get(pk=pk)
                reservation.vehicle = vehicle
                reservation.client_name = client_name
                reservation.departure_dt = departure_dt
                reservation.return_dt = return_dt
                reservation.details = details
                reservation.save()
            except Reservation.DoesNotExist:
                pass
        else:
            reservation = Reservation(
                vehicle = vehicle,
                client_name = client_name,
                departure_dt = departure_dt,
                return_dt = return_dt,
                details = details
            )
            reservation.save()

        return redirect("reservations")

    # request.method == "GET"
    else:
        reservation = None
        update_flag = False

        if pk:
            try:
                reservation = Reservation.objects.get(pk=pk)
                update_flag = True
            except Reservation.DoesNotExist:
                # Redirect to create a new one
                return redirect("crud_reservation")

        vehicles = [vehicle for vehicle in Vehicle.objects.all()]

        default_departure_dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        default_return_dt = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)

        context = {
            "reservation": reservation,
            "update_flag": update_flag,
            "vehicles": vehicles,
            "default_departure_dt": default_departure_dt,
            "default_return_dt": default_return_dt
        }

    return render(request, "crud_reservation.html", context)

def delete_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
        reservation.delete()
    except Reservation.DoesNotExist:
        pass
        # Redirect to create a new one
    return redirect("reservations")

def reservations(request):
    reservations = Reservation.objects.all().order_by("-pk")
    context = {
        "reservations": reservations
    }

    return render(request, "reservations.html", context)
