from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


# Create your views here.
def checkout(request):
    # first, get GET-params
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("products"))
    
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
    }
    return render(request, template, context)
