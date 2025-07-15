from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Product, Series, Fit, Occasion, Color, Category, ProductVariant
from django.http import Http404
import json


# Create your views here.
def products(request):
    """A view to return products page which filters/sorts the products from the products list"""
    # read in the models
    products = Product.objects.filter(is_active=True).prefetch_related('variants')
    series_list = Series.objects.all()
    fit_list = Fit.objects.all()
    occasion_list = Occasion.objects.all()
    colors_list = Color.objects.all()
    colors_list = Color.objects.annotate(variant_count=Count('productvariant'))
    categories_list = Category.objects.all()
    fabrics_list = Product.objects.values_list('fabric', flat=True).distinct()
    
    # read in the GET-method params
    query = request.GET.get("q")
    selected_categories = request.GET.getlist('category')
    selected_fits = request.GET.getlist('fit')
    selected_occasions = request.GET.getlist('occasion')
    selected_fabrics = request.GET.getlist('fabric')
    selected_colors = request.GET.getlist('colors')
    selected_series = [int(s) for s in request.GET.getlist('series') if s.strip() != '']

    # handle query
    if (query):
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(series__name__icontains=query) |
            Q(series__description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(variants__fit__name__icontains=query) |
            Q(variants__size__name__icontains=query) |
            Q(variants__color__name__icontains=query)
        ).distinct()
    
    # apply each filter
    if selected_categories:
        products = products.filter(category__name__in=selected_categories)
        
    if selected_occasions:
        products = products.filter(occasion__name__in=selected_occasions)
    
    if selected_series:
        products = products.filter(series__id__in=selected_series)
    
    if selected_colors:
        products = products.filter(variants__color__name__in=selected_colors)
        
    if selected_fits:
        products = products.filter(variants__fit__name__in=selected_fits)
    
    if selected_fabrics:
        products = products.filter(fabric__in=selected_fabrics)  # no foreignkey -> Charfield only
    
    products = products.distinct()

    # set min/max prices for each product (my model doesn't have prices for
    # products - only for variants TO PREVENT DUPLICATES+REDUNDANT DATA)
    # should be after the filters (they overwrite them?)
    for p in products:
        variants = p.variants.all()
        p.min_price = min([v.price for v in variants], default=None)
        p.max_price = max([v.price for v in variants], default=None)
        print(f"MINIMUM PRICE {p.name}: {p.min_price}")
    
    context = {
        'products': products,
        'search_term': query,
        'series_list': series_list,
        'fit_list': fit_list,
        'occasion_list': occasion_list,
        'colors_list': colors_list,
        'categories_list': categories_list,
        'fabrics_list': fabrics_list,
        'selected_categories': selected_categories, 
        'selected_fits': selected_fits, 
        'selected_occasions': selected_occasions, 
        'selected_fabrics': selected_fabrics, 
        'selected_colors': selected_colors, 
        'selected_series': selected_series, 
        
    }
    
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """A view to show all products details necessary to decide whether to buy a product or not"""

    # first, load from the db..
    product = get_object_or_404(Product, pk=product_id)
    variants = ProductVariant.objects.filter(product=product)

    # get distinct variant's options so that the user can select options
    # important: not all combinations can be selected - later in the 
    # template/js, this must be managed with the help of variants list
    sizes = variants.values_list("size__name", flat=True).distinct()
    colors = variants.values("color__name", "color__hex_code").distinct()  # --------------------incorrect
    fits = variants.values_list("fit__name", flat=True).distinct()
    
    # nice feature: the customer will be offered other products of the same series
    more_from_series = Product.objects.filter(series=product.series).exclude(id=product.id)
    
    # retrieve the min-price for a product (because the prices are stored in ProductVariant)
    for p in more_from_series:
        p.min_price = min([v.price for v in p.variants.all()], default=None)
        p.max_price = max([v.price for v in p.variants.all()], default=None)
        print(f"Rating: {p.name}: {p.rating}")
    
    # now, we have to choose a variant to load - it's better in the url than in JS
    variant_id = request.GET.get("variant")
    if variant_id:
        try:
            selected_variant = variants.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            selected_variant = variants.first()
    else:
        selected_variant = variants.first()
        if selected_variant:
            return redirect(f"{request.path}?variant={selected_variant.id}")
        else:
            raise Http404("No variants available for this product. Please choose another product.")
    
    # create a json so that the template can hand over the list to JS so that it can build new urls based on
    # the user's selection (e.g. change color -> create new url and reload, this view will then take the new variant id)
    variant_options = [
        {
            "id": v.id,
            "size": v.size.name,
            "color": v.color.name,
            "fit": v.fit.name,
            "price": float(v.price),
        }
        for v in variants
    ]
    variant_options_json = json.dumps(variant_options)
    
    max_qty = min(selected_variant.stock, 10)
    
    context = {
        "max_qty": max_qty,
        'qty_range': range(1, max_qty+1),
        'product': product,
        'variants': variants,
        'selected_variant': selected_variant,
        'more_from_series': more_from_series,
        'variant_options_json': variant_options_json,
        'sizes': sizes,
        'colors': colors,
        'fits': fits,
    }

    return render(request, 'products/product_details.html', context)
