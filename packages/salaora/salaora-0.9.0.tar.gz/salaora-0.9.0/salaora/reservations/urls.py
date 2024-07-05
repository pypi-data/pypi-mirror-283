from django.urls import path

from reservations import views

urlpatterns = [
    path("crud_reservation", views.crud_reservation, name="crud_reservation"),
    path("crud_reservation/<int:pk>", views.crud_reservation, name="crud_reservation"),
    path("reservations", views.reservations, name="reservations"),
    path("delete_reservation/<int:pk>", views.delete_reservation, name="delete_reservation")
]
