from django.shortcuts import render

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg, Max, F, Q, Value, DecimalField
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

STATUS_CREATED = "created"
STATUS_CONFIRMED = "confirmed"
STATUS_DENIED = "denied"
STATUS_SENT = "sent"
STATUS_RETURNED = "returned"


@staff_member_required
def dashboard(request):
    now = timezone.now()
    two_day_ago = now - timedelta(days=2)
    three_days_ago = now - timedelta(days=3)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # collect data for the products card..

    # collect data for the orders card..

    # collect data for the sales card

    # collect data for the graph

    # collect data for the top10 sales (by variant)

    # collect data for the users' card

    context = {
        # products

        # orders

        # sales

        # top 10

        # users
    }

    return render(request, "business_center/business_center.html", context)
