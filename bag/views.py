from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from .models import Variant


# Create your views here.
def view_bag(request):
    """A view to render a shopping bag page"""

    context = {}

    return render(request, 'bag/bag.html', context)


def add_to_bag(request):
    """Add the selected variant to the shopping bag"""
    
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))
        redirect_url = request.POST.get("redirect_url", "/")

        # variant = get_object_or_404(Variant, pk=variant_id)

        bag = request.session.get("bag", {})

        if variant_id in bag:
            bag[variant_id] += quantity
        else:
            bag[variant_id] = quantity

        request.session["bag"] = bag

        return redirect(redirect_url)


def update_bag(request, variant_id):
    """Update quantity of a variant in the bag"""
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        redirect_url = request.POST.get("redirect_url", "/")
        print(redirect_url)
        bag = request.session.get("bag", {})

        if quantity > 0:
            bag[str(variant_id)] = quantity
            messages.success(request, "Quantity updated successfully.")
        else:
            bag.pop(str(variant_id), None)
            messages.success(request, "Item removed from bag.")

        request.session["bag"] = bag
        
        return redirect(redirect_url)


def remove_from_bag(request, variant_id):
    """Remove a variant from the bag"""
    redirect_url = request.POST.get("redirect_url", "/")

    bag = request.session.get("bag", {})
    bag.pop(str(variant_id), None)

    request.session["bag"] = bag
    messages.success(request, "Item removed from bag.")
    return redirect(redirect_url)