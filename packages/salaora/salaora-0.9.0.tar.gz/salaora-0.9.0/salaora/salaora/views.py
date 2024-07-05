from datetime import datetime

from django.shortcuts import render
from django.shortcuts import redirect

from django.db.models import Q

from reservations.models import Reservation
from vehicles.models import Vehicle

def index(request):

    today_dt = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    now_dt = datetime.now()

    q_returns_today = Q(return_dt__date=today_dt)
    q_returns_later = Q(return_dt__gt=now_dt)
    today_pending_returns = Reservation.objects.filter(q_returns_today & q_returns_later).order_by("return_dt")

    q_departures_today = Q(departure_dt__date=today_dt)
    q_departures_later = Q(departure_dt__gt=now_dt)
    today_pending_departures = Reservation.objects.filter(q_departures_today & q_departures_later).order_by("departure_dt")

    context = {
        "today_pending_returns": today_pending_returns,
        "today_pending_departures": today_pending_departures
    }
    return render(request, "index.html", context)
