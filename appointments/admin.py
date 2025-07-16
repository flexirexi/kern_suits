from django.contrib import admin
from .models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "appointment_type",
        "start_datetime",
    )
    list_filter = (
        "appointment_type",
        "start_datetime",
    )
    search_fields = (
        "user__username",
        "comment",
    )
    ordering = (
        "start_datetime",
    )
