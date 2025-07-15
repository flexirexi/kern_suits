from decimal import Decimal
from django.conf import settings
from products.models import ProductVariant
from django.shortcuts import get_object_or_404


def bag_contents(request):
    bag = request.session.get("bag", {})

    bag_items = []
    total = 0
    variant_count = 0
    delivery_cost = 0
    
    for variant_id_str, quantity in bag.items():
        variant_id = int(variant_id_str)
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        
        subtotal = variant.price * quantity
        total += subtotal
        variant_count += quantity
        delivery_cost = 0
        
        bag_items.append({
            "variant": variant,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    context = {
        "bag_items": bag_items,
        "grand_total": total,
        "variant_count": variant_count,
        "delivery_cost": delivery_cost,
    }
    
    return context
