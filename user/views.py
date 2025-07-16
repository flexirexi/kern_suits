from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, timezone

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order, OrderItem
from appointments.models import Appointment


# Create your views here.
@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # personal data
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "New profile data saved!")
    else:
        form = UserProfileForm(instance=profile)

    # all orders of the user
    order_items = (
        OrderItem.objects.filter(order__user=request.user)
        .select_related(
            'order', 
            'variant__product', 
            'variant__size', 
            'variant__product__occasion', 
            'variant__color', 
            'variant__fit'
        )
        .order_by('-order__created_at')
    )

    # calculate delivery status
    # since there is no 'real' delivery, I have to pre-set delivery status:
    today = date.today()
    order_items_with_status = []

    for item in order_items:
        order_date = item.order.created_at.date() if item.order.created_at else today
        days_since_order = (today - order_date).days

        if days_since_order >= 3:
            status = "Delivered"
        elif days_since_order >= 1:
            status = "Shipped"
        else:
            status = "In Progress"

        # Custom Attribut anhängen
        item.delivery_status = status

        order_items_with_status.append(item)
    
    context = {
        'form': form,
        'order_items': order_items_with_status,  # manually calculated status
    }
    return render(request, 'user/profile.html', context)


@login_required
def order_details(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    print(f"ORDER: {order.user}")
    order_items = (
        OrderItem.objects.filter(order=order)
        .select_related(
            'variant__product',
            'variant__size',
            'variant__fit',
            'variant__color'
        )
        .order_by('id')
    )

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'user/order_details.html', context)


@login_required
def manage_appointments(request):
    user_appointments = Appointment.objects.filter(user=request.user).order_by("start_datetime")

    today = date.today()
    cancel_threshold = today + timedelta(days=7)
    
    context = {
        "user_appointments": user_appointments,
        "today": today,
        "cancel_threshold": cancel_threshold,
    }
    return render(request, "user/manage_appointments.html", context)


@login_required
def edit_appointment(request, appt_id):
    appointment = get_object_or_404(Appointment, id=appt_id, user=request.user)

    today = date.today()
    cancel_threshold = today + timedelta(days=7)

    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        appointment.comment = comment
        appointment.save()
        messages.success(request, "Appointment updated successfully.")
        return redirect("manage_appointments")  
        
    context = {
        "appointment": appointment,
        "cancel_threshold": cancel_threshold,
    }
    return render(request, "user/edit_appointment.html", context)


@login_required
def delete_appointment(request, appt_id):
    appointment = get_object_or_404(Appointment, id=appt_id, user=request.user)
    appointment.delete()
    messages.info(request, "Appointment deleted successfully.")
    return redirect("manage_appointments")
