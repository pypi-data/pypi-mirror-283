from django.contrib import admin

from vehicles.models import Vehicle

class VehicleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vehicle, VehicleAdmin)
