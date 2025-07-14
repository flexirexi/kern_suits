from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from .models import Product, Series, Fit, Occasion, Color, Category


# Create your views here.
def products(request):
    """A view to return products page which filters/sorts the products from the products list"""
    
    products = Product.objects.filter(is_active=True).prefetch_related('variants')
    series_list = Series.objects.all()
    fit_list = Fit.objects.all()
    occasion_list = Occasion.objects.all()
    colors_list = Color.objects.all()
    colors_list = Color.objects.annotate(variant_count=Count('productvariant'))
    categories_list = Category.objects.all()
    
    query = request.GET.get("q")
    
    for p in products:
        variants = p.variants.all()
        p.min_price = min([v.price for v in variants], default=None)
        p.max_price = max([v.price for v in variants], default=None)
    
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
