from django.shortcuts import render

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg, Max, F, Q, Value, DecimalField
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from checkout.models import Order, OrderItem
from products.models import Product, ProductVariant, Series

STATUS_CREATED = "created"
STATUS_CONFIRMED = "confirmed"
STATUS_DENIED = "denied"
STATUS_SENT = "sent"
STATUS_RETURNED = "returned"


@staff_member_required
def dashboard(request):
    now = timezone.now()
    two_days_ago = now - timedelta(days=2)
    three_days_ago = now - timedelta(days=3)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # collect data for the products card ----------------------
    total_products = Product.objects.count()
    total_variants = ProductVariant.objects.count()
    series_in_stock = (
        Series.objects.filter(
            is_active=True,
            products__is_active=True,
            products__variants__stock__gt=0,
        )
        .distinct()
        .count()
    )

    # collect data for the orders card ---------------------------
    unconfirmed_total = Order.objects.filter(status=STATUS_CREATED).count()
    unconfirmed_gt2 = Order.objects.filter(
        status=STATUS_CREATED,
        created_at__lte=two_days_ago
    ).count()

    confirmed_total = Order.objects.filter(status=STATUS_CONFIRMED).count()
    confirmed_gt3 = Order.objects.filter(
        status=STATUS_CONFIRMED,
        created_at__lte=three_days_ago
    ).count()

    denied_total = Order.objects.filter(status=STATUS_DENIED).count()
    denied_month = Order.objects.filter(
        status=STATUS_DENIED,
        created_at__gte=start_of_month
    ).count()

    sent_total = Order.objects.filter(status=STATUS_SENT).count()
    sent_month = Order.objects.filter(
        status=STATUS_SENT,
        created_at__gte=start_of_month
    ).count()

    # collect data for the sales card ---------------------------

    # collect data for the graph -------------------------------

    # collect data for the top10 sales (by variant) -----------------

    # collect data for the users' card ---------------------------

    context = {
        # products
        "total_products": total_products,
        "total_variants": total_variants,
        "series_in_stock": series_in_stock,

        # orders
        "unconfirmed_total": unconfirmed_total,
        "unconfirmed_gt2": unconfirmed_gt2,
        "confirmed_total": confirmed_total,
        "confirmed_gt3": confirmed_gt3,
        "denied_total": denied_total,
        "denied_month": denied_month,
        "sent_total": sent_total,
        "sent_month": sent_month,

        # sales

        # top 10

        # users
    }

    return render(request, "business_center/business_center.html", context)
