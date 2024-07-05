from django.urls import path

from vehicles import views

urlpatterns = [
    path("", views.vehicles, name="vehicles"),
    path("vehicle/<str:pk>", views.vehicle, name="vehicle"),
    path("vehicles", views.vehicles, name="vehicles"),
    path("bulk_create_vehicles", views.bulk_create_vehicles, name="bulk_create_vehicles"),
]
