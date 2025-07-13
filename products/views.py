from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


# Create your views here.
def products(request):
    """A view to return products page which filters/sorts the products from the products list"""
    
    products = Product.objects.all()
    query = request.GET.get("q")
    
    products = Product.objects.filter(
        is_active=True
    )
    
    context = {
        'products': products,
        'search_term': query,
    }
    
    return render(request, 'products/products.html', context)
