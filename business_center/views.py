from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    HttpRequest
)

from datetime import timedelta
from decimal import Decimal


from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum, Avg, Max, F, Q, Value, DecimalField
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from checkout.models import Order, OrderItem
from products.models import Product, ProductVariant, Series, Category

from django.contrib import messages
from .forms import ProductVariantForm

from dataclasses import dataclass

STATUS_CREATED = "created"
STATUS_CONFIRMED = "confirmed"
STATUS_DENIED = "denied"
STATUS_SENT = "sent"
STATUS_RETURNED = "returned"

# new:
STATUS_DELIVERED = "delivered"
STATUS_LOST = "lost"


@dataclass(frozen=True)
class DateRangeOption:
    key: str
    label: str


RANGE_OPTIONS = [
    DateRangeOption("3", "≤ 3 days (last 3 days)"),
    DateRangeOption("7", "≤ 7 days (last week)"),
    DateRangeOption("30", "≤ 30 days (last 30 days)"),
    DateRangeOption("gt30", "> 30 days"),
]


def _apply_day_range_filter(qs, field_name: str, range_key: str):
    """
    Filters by date() only (no time) - for orders.html
    range_key in {"3","7","30","gt30",""}.
    """
    if not range_key:
        return qs

    today = timezone.localdate()
    if range_key == "gt30":
        cutoff = today - timedelta(days=30)
        return qs.filter(**{f"{field_name}__date__lt": cutoff})

    try:
        days = int(range_key)
    except ValueError:
        return qs

    cutoff = today - timedelta(days=days)
    return qs.filter(**{f"{field_name}__date__gte": cutoff})


def _decorate_orders_for_ui(orders):
    """
    Adds computed UI-only attributes (for orders.html):
    - items_count
    - updated_days_ago
    - effective_status ("delivered" if sent and updated >= 3 days)
    - dot_color ("green/yellow/orange/red")
    """
    today = timezone.localdate()

    for o in orders:
        o.items_count = sum(i.quantity for i in o.items.all())
        updated_date = o.updated_at.date() if o.updated_at else today
        o.updated_days_ago = (today - updated_date).days

        if o.status == "sent" and o.updated_days_ago >= 3:
            o.effective_status = "delivered"
        else:
            o.effective_status = o.status

        # Dot logic
        if o.effective_status == "delivered":
            o.dot_color = "green"
        else:
            if o.updated_days_ago > 7:
                o.dot_color = "red"
            elif o.updated_days_ago > 3:
                o.dot_color = "orange"
            else:
                o.dot_color = "yellow"

    return orders


@login_required
def bc_orders_management(request: HttpRequest):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only staff/superuser may be able to enter the business center."
        )

    qs = (
        Order.objects
        .prefetch_related("items__variant", "items__variant__product")
        .order_by("-created_at")
    )

    status = request.GET.get("status", "").strip()
    created_range = request.GET.get("created", "").strip()
    updated_range = request.GET.get("updated", "").strip()

    if status:
        qs = qs.filter(status=status)

    qs = _apply_day_range_filter(qs, "created_at", created_range)
    qs = _apply_day_range_filter(qs, "updated_at", updated_range)

    orders = list(qs[:500])  # hard cap: keeps page snappy

    orders = _decorate_orders_for_ui(orders)

    context = {
        "orders": orders,
        "status": status,
        "created_range": created_range,
        "updated_range": updated_range,
        "range_options": RANGE_OPTIONS,
        "status_choices": [
            ("", "All"),
            ("created", "Created"),
            ("confirmed", "Confirmed"),
            ("denied", "Denied"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("returned", "Returned"),
        ],
    }
    return render(request, "business_center/orders_management.html", context)


@require_POST
@login_required
def bc_orders_bulk_action(request: HttpRequest):
    """
    POST JSON or form-encoded:
    - action: "confirm" | "deny" | "sent" | "returned" | "mark_lost"
    - order_ids[]: list of ids
    """
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only staff/superuser may be able to enter the business center."
        )

    action = request.POST.get("action", "").strip()
    order_ids = request.POST.getlist("order_ids[]") or request.POST.getlist(
        "order_ids"
    )

    if not action or not order_ids:
        return JsonResponse(
            {
                "ok": False,
                "error": "Missing action or order_ids."
            }, status=400)

    qs = Order.objects.filter(id__in=order_ids)

    # Load orders to validate action rules
    orders = list(qs)
    if not orders:
        return JsonResponse(
            {
                "ok": False,
                "error": "No matching orders."
            }, status=404)

    # Determine effective_status same as UI (for rule checks)
    today = timezone.localdate()

    def effective_status(order: Order) -> str:
        updated_date = order.updated_at.date() if order.updated_at else today
        days_ago = (today - updated_date).days
        if order.status == "sent" and days_ago >= 3:
            return "delivered"
        return order.status

    # Action rules:
    # - confirm: only if status in {"created", "denied"}
    # - deny: only if effective_status is NOT "sent" or "delivered"
    #   when the package is on the way, it cant be denied
    # - sent: only if status == "confirmed" (reasonable default)
    # - returned: always allowed
    # - mark_lost: enabled for sent/delivered
    def all_in_allowed(allowed: set[str]) -> bool:
        return all(o.status in allowed for o in orders)

    if action == "confirm":
        if not all_in_allowed({"created", "denied"}):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Confirm allowed only for Created/Denied."
                }, status=400)
        new_status = "confirmed"

    elif action == "deny":
        if any(effective_status(o) in {"sent", "delivered"} for o in orders):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Cannot deny orders already sent."
                }, status=400)
        new_status = "denied"

    elif action == "sent":
        if not all_in_allowed({"confirmed"}):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Sent allowed only for Confirmed orders."
                }, status=400)
        new_status = "sent"

    elif action == "returned":
        new_status = "returned"

    elif action == "mark_lost":
        # better term than "report as loss"
        if any(
            effective_status(o) not in {"sent", "delivered"} for o in orders
        ):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Mark as lost only for sent/delivered orders."
                }, status=400)

        # For now: reuse 'returned' would be misleading, so we store 'denied'
        # is also misleading.
        # Best minimal option: add "lost" status (no DB migration needed).
        new_status = "lost"

    else:
        return JsonResponse(
            {
                "ok": False,
                "error": "Unknown action."
            }, status=400)

    with transaction.atomic():
        qs.update(status=new_status)

    # Emails later (Mailchimp) — intentionally not implemented now.
    messages.success(
        request,
        f"Updated {len(orders)} order(s) -> {new_status}."
    )
    return JsonResponse(
        {
            "ok": True,
            "updated": len(orders),
            "new_status": new_status
        }
    )


@login_required
def dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden(
            "Only staff/superuser may be able to enter the business center."
        )
    now = timezone.now()
    two_days_ago = now - timedelta(days=2)
    three_days_ago = now - timedelta(days=3)
    start_of_month = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)

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
    sent_orders = Order.objects.filter(status=STATUS_SENT)

    zero_dec = Value(Decimal("0.00"), output_field=DecimalField(
        max_digits=12, decimal_places=2))
    sales_total = sent_orders.aggregate(
        total=Coalesce(Sum("grand_total"), zero_dec))["total"]
    sales_avg = sent_orders.aggregate(
        avg=Coalesce(Avg("grand_total"), zero_dec))["avg"]
    sales_max = sent_orders.aggregate(
        max=Coalesce(Max("grand_total"), zero_dec))["max"]
    sales_count = sent_orders.count()

    # collect data for the graph -------------------------------
    series_qs = (
        sent_orders.annotate(period=TruncMonth("created_at"))
        .values("period")
        .annotate(total=Coalesce(Sum("grand_total"), zero_dec))
        .order_by("period")
    )
    series_list = list(series_qs)
    max_series_total = max(
        [row["total"] for row in series_list], default=Decimal("1.00")
    )

    def to_decile(total):
        if max_series_total <= 0 or total <= 0:
            return 0
        pct = float((total / max_series_total) * 100.0)
        dec = int(round(pct / 10.0)) * 10
        return max(0, min(100, dec))

    sales_series = [{
        "label": row["period"].strftime("%b %Y"),
        "total": row["total"],
        "pct": (
            float((row["total"] / max_series_total) * 100)
            if max_series_total > 0
            else 0.0
        ),
    }
        for row in series_list
    ]

    # collect data for the top10 product variant sales (by variant) ----------
    revenue_expr = F("quantity") * F("price")
    zero_dec_big = Value(Decimal("0.00"), output_field=DecimalField(
        max_digits=14, decimal_places=2))
    top_variants = (
        OrderItem.objects.filter(order__status=STATUS_SENT)
        .values(
            "variant__sku",
            "variant__product__name",
            "variant__size__name",
            "variant__fit__name",
            "variant__color__name",
        )
        .annotate(
            units=Coalesce(Sum("quantity"), Value(0)),
            revenue=Coalesce(Sum(revenue_expr, output_field=DecimalField(
                max_digits=14, decimal_places=2)), zero_dec_big),
        )
        .order_by("-revenue")[:10]
    )

    # collect data for the users' card ---------------------------
    User = get_user_model()
    users_total = User.objects.count()
    users_staff = User.objects.filter(is_staff=True).count()
    users_admin = User.objects.filter(is_superuser=True).count()

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
        "sales_total": sales_total,
        "sales_avg": sales_avg,
        "sales_max": sales_max,
        "sales_count": sales_count,
        "sales_series": sales_series,

        # top 10
        "top_variants": top_variants,

        # users
        "users_total": users_total,
        "users_staff": users_staff,
        "users_admin": users_admin,
    }

    return render(request, "business_center/business_center.html", context)


@login_required
def product_management(request):
    qs = ProductVariant.objects.select_related(
        "product", "product__series", "fit", "size", "color"
    )

    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers may change rights.")

    # Filters/search
    q = request.GET.get("q", "")
    if q:
        qs = qs.filter(
            Q(product__name__icontains=q) |
            Q(product__series__name__icontains=q) |
            Q(size__name__icontains=q) |
            Q(fit__name__icontains=q) |
            Q(color__name__icontains=q) |
            Q(product__fabric__icontains=q)
        )

    sel_series = request.GET.getlist(
        "series") or [request.GET.get("series", "")]
    sel_series = [int(s) for s in sel_series if s]
    if sel_series:
        qs = qs.filter(product__series__id__in=sel_series)

    sel_cat = request.GET.getlist("category") or [
        request.GET.get("category", "")]
    sel_cat = [c for c in sel_cat if c]
    if sel_cat:
        qs = qs.filter(product__category__name__in=sel_cat)

    sel_fabric = request.GET.getlist(
        "fabric") or [request.GET.get("fabric", "")]
    sel_fabric = [f for f in sel_fabric if f]
    if sel_fabric:
        qs = qs.filter(product__fabric__in=sel_fabric)

    context = {
        "variants": qs.order_by("product__name", "size__name"),
        "series_list": Series.objects.all(),
        "categories_list": Category.objects.all(),
        "fabrics_list": Product.objects.values_list(
            "fabric", flat=True
        ).distinct(),
        "search_term": q,
        "selected_series": sel_series,
        "selected_categories": sel_cat,
        "selected_fabrics": sel_fabric,
    }

    return render(request, "business_center/product_management.html", context)


@require_POST
def variant_plus(request, pk):
    v = get_object_or_404(ProductVariant, pk=pk)
    v.stock = (v.stock or 0) + 1
    v.save(update_fields=["stock"])
    return JsonResponse({"stock": v.stock, "message": "Quantity increased."})


@require_POST
def variant_minus(request, pk):
    v = get_object_or_404(ProductVariant, pk=pk)
    v.stock = max(0, (v.stock or 0) - 1)
    v.save(update_fields=["stock"])
    return JsonResponse({"stock": v.stock, "message": "Quantity reduced."})


@require_POST
def variant_duplicate(request, pk):
    v = get_object_or_404(ProductVariant, pk=pk)
    v.pk = None
    v.stock = 0
    v.save()
    return JsonResponse({"message": "Variant duplicated."})


@require_POST
def variant_remove(request, pk):
    v = get_object_or_404(ProductVariant, pk=pk)
    v.delete()
    return JsonResponse({"message": "Variant deleted."})


def variant_edit(request, pk):
    return redirect("admin:app_productvariant_change", pk)


def variant_create(request):
    if request.method == "POST":
        form = ProductVariantForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                form.add_error(None, str(e))
            else:
                messages.success(request, "Variant erstellt.")
                return redirect("bc_product_management")
    else:
        form = ProductVariantForm()

    return render(request, "business_center/variant_form.html", {"form": form})


@login_required
# staff may view; superuser can modify (see toggle view)
@user_passes_test(lambda u: u.is_staff)
def user_rights(request):
    role = request.GET.get("role", "").strip().lower()
    qs = User.objects.all().order_by("username")

    if role == "admin":
        qs = qs.filter(is_superuser=True)
    elif role == "staff":
        # as requested: only filter by is_staff
        qs = qs.filter(is_staff=True)
    elif role == "customer":
        qs = qs.filter(is_staff=False, is_superuser=False)

    context = {
        "users": qs,
        "role": role,
        "can_edit": request.user.is_superuser,  # superuser only
    }
    return render(request, "business_center/user_rights.html", context)


@login_required
@require_POST
def user_rights_toggle(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers may change rights.")

    target = get_object_or_404(User, pk=pk)
    field = request.POST.get("field")
    value = request.POST.get("value")

    if field not in {"is_active", "is_staff", "is_superuser"}:
        return HttpResponseBadRequest("Invalid field.")
    val = value in ("1", "true", "True", "on")

    # Safety: don’t let a user remove their own superuser/active status
    if target.id == request.user.id and (
        field in {"is_superuser", "is_active"} and not val
    ):
        return HttpResponseBadRequest(
            "You cannot change this status on yourself."
        )

    # Apply change
    setattr(target, field, val)

    # Invariant: superuser implies staff
    if field == "is_superuser" and val is True:
        target.is_staff = True
    # Optional: prevent 'superuser but not staff'
    if field == "is_staff" and val is False and target.is_superuser:
        # either force superuser off, or reject — here we reject:
        return HttpResponseBadRequest(
            "Superuser must also be staff. Uncheck superuser first."
        )

    target.save(
        update_fields=[
            "is_active", "is_staff", "is_superuser"
        ] if field == "is_superuser" else [field])

    return JsonResponse({
        "ok": True,
        "user_id": target.id,
        "is_active": target.is_active,
        "is_staff": target.is_staff,
        "is_superuser": target.is_superuser,
    })
