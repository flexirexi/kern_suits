from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Product, Series, Fit, Occasion, Color, Category


# Create your views here.
def products(request):
    """A view to return products page which filters/sorts the products from the products list"""
    # read the models
    products = Product.objects.filter(is_active=True).prefetch_related('variants')
    series_list = Series.objects.all()
    fit_list = Fit.objects.all()
    occasion_list = Occasion.objects.all()
    colors_list = Color.objects.all()
    colors_list = Color.objects.annotate(variant_count=Count('productvariant'))
    categories_list = Category.objects.all()
    
    # read the GET-method params
    query = request.GET.get("q")
    categories = request.GET.getlist('category')
    fit = request.GET.getlist('fit')
    occasion = request.GET.getlist('occasion')
    fabric = request.GET.getlist('fabric')
    color = request.GET.getlist('colors')
    series = [int(s) for s in request.GET.getlist('series') if s.strip() != '']

    print(f"CATEGORIES: {len(categories)} --------------")
    print(f"FIT: {len(fit)} --------------")
    print(f"OCCASION: {len(occasion)} --------------")
    print(f"FABRIC: {len(fabric)} --------------")
    print(f"COLOR: {len(color)} --------------")
    print(f"SERIES: {len(series)} --------------")

    # apply each filter
    if categories:
        products = products.filter(category__name__in=categories)
        
    if occasion:
        products = products.filter(occasion__name__in=occasion)
    
    if series:
        products = products.filter(series__id__in=series)
    
    if color:
        products = products.filter(variants__color__name__in=color)
        
    if fit:
        products = products.filter(variants__fit__name__in=fit)
    
    if fabric:
        products = products.filter(fabric__in=fabric) #  no foreignkey -> Charfield only
    
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
    }
    
    return render(request, 'products/products.html', context)
