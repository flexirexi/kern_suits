from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import OrderItem


# Create your views here.
@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # Persönliche Daten bearbeiten
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "New profile data saved!")
    else:
        form = UserProfileForm(instance=profile)

    # Alle OrderItems des Users
    order_items = (
        OrderItem.objects.filter(order__user=request.user)
        .select_related('order', 'variant__product', 'variant__size', 'variant__product__occasion', 'variant__color', 'variant__fit')
        .order_by('-order__created_at')
    )

    context = {
        'form': form,
        'order_items': order_items,
    }
    return render(request, 'user/profile.html', context)