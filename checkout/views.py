from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import OrderForm
from bag.contexts import bag_contents
from .models import Order, OrderItem
from products.models import Product, ProductVariant
# from user.forms import UserProfileForm
from user.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


# Create your views here.
def checkout(request):
    # get stripe keys
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    # get GET-params
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("products"))
    
    # getting stripe done
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)  # stripe uses amounts as integers
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')
    
    # get POST-forms
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # some stuff here
            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    form = OrderForm(initial={
                        'first_name': profile.user.first_name,
                        'last_name': profile.user.last_name,
                        'email': profile.user.email,
                        'phone_number': profile.phone_number,
                        'country': profile.country,
                        'postcode': profile.postcode,
                        'town_or_city': profile.town_or_city,
                        'street_address1': profile.street_address1,
                        'street_address2': profile.street_address2,
                        'county': profile.county,
                    })
                except UserProfile.DoesNotExist:
                    form = OrderForm()
    else:
        form = OrderForm()
    
    template = "checkout/checkout.html"
    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    try:
        data = json.loads(request.body)
        pid_raw = data.get('client_secret')
        if not pid_raw:
            return HttpResponse("Missing client_secret", status=400)

        pid = pid_raw.split('_secret')[0]
        # pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': data.get('save_info'),
            'username': str(request.user),
        })
        return JsonResponse({"status": "ok"})
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=f"Error: {str(e)}", status=400)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        # if save_info:
        #     profile_data = {
        #         'phone_number': order.phone_number,
        #         'country': order.country,
        #         'postcode': order.postcode,
        #         'town_or_city': order.town_or_city,
        #         'street_address1': order.street_address1,
        #         'street_address2': order.street_address2,
        #         'county': order.county,
        #     }
        #     user_profile_form = UserProfileForm(profile_data, instance=profile)
        #     if user_profile_form.is_valid():
        #         user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
