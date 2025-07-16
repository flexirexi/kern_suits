from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date, timedelta, datetime

from .forms import AppointmentForm
from .models import Appointment


# Create your views here.
@login_required
def appointments(request):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    all_appointments = Appointment.objects.all()
    user_appointments = Appointment.objects.filter(user=request.user)
    
    booked_slots = {}

    for appt in all_appointments:
        date_key = appt.start_datetime.date().isoformat()
        hour = appt.start_datetime.hour
        booked_slots.setdefault(date_key, []).append(hour)
        
    opening_hours = settings.OPENING_HOURS
    form = AppointmentForm()
    
    # take care of POST methods
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            start_dt_str = request.POST.get("start_datetime")
            
            if not start_dt_str:
                messages.error(request, "No date/ time selected.")
            else:
                try:
                    start_dt = datetime.fromisoformat(start_dt_str)
                except ValueError:
                    messages.error(request, "invalid time/date format..")
                else:
                    appointment = form.save(commit=False)
                    appointment.user = request.user
                    appointment.start_datetime = start_dt
                    appointment.save()
                    messages.success(request, "Booking successfully.")
                    return redirect("appointments")
    
    else:
        form = AppointmentForm()
    
    context = {
        "all_appointments": all_appointments,
        "user_appointments": user_appointments,
        "opening_hours": opening_hours,
        "booked_slots": booked_slots,
        "today": today.isoformat(),
        "tomorrow": tomorrow.isoformat(),
        "form": form,
    }
    return render(request, "appointments/appointments.html", context)
