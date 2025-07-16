from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from .models import Appointment


# Create your views here.
@login_required
def appointment_calendar(request):
    all_appointments = Appointment.objects.all()
    user_appointments = Appointment.objects.filter(user=request.user)
    opening_hours = settings.OPENING_HOURS

    context = {
        "all_appointments": all_appointments,
        "user_appointments": user_appointments,
        "opening_hours": opening_hours,
    }
    return render(request, "appointments/calendar.html", context)
