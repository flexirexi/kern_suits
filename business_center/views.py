from django.shortcuts import render, get_object_or_404, redirect

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Sum, Avg, Max, F, Q, Value, DecimalField
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from checkout.models import Order, OrderItem
from products.models import Product, ProductVariant, Series, Category

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from .forms import ProductVariantForm

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
    max_series_total = max([row["total"]
                           for row in series_list], default=Decimal("1.00"))

    def to_decile(total):
        if max_series_total <= 0 or total <= 0:
            return 0
        pct = float((total / max-series_total) * 100.0)
        dec = int(round(pct / 10.0)) * 10
        return max(0, min(100, dec))

    sales_series = [{
        "label": row["period"].strftime("%b %Y"),
        "total": row["total"],
        "pct": float((row["total"] / max_series_total) * 100) if max_series_total > 0 else 0.0,
    }
        for row in series_list
    ]

    # collect data for the top10 product variant sales (by variant) -----------------
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


def product_management(request):
    qs = ProductVariant.objects.select_related(
        "product", "product__series", "fit", "size", "color"
    )

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
        "fabrics_list": Product.objects.values_list("fabric", flat=True).distinct(),
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
