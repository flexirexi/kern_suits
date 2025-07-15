from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


# Create your views here.

# Create your views here.
def checkout(request):
    # first, get GET-params
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("products"))
    
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total *100) # stripe uses amounts as integers
    
    # get POST-forms
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # some stuff here
            pass
    else:
        form = OrderForm()
    
    template = "checkout/checkout.html"
    context = {
        'form': form,
        'stripe_public_key': '51RiMXjBG5LZ2QZIIYu8KYHeqkKnmdjMPHO8Y3RjvsrEO5mFT5tBMhu65U9Nx7EeIhdjdmw7QSIBbUTglBVXRWBRn000SIcw5cH',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
