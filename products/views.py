from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import ProductVariant


# Create your views here.
def products(request):
    """A view to return products page which filters/sorts the products from the products list"""
    
    productVariants = ProductVariant.objects.all()
    query = request.GET.get("q")
    
    productVariants = ProductVariant.objects.filter(
        is_active=True,
        product__is_active=True
    )
    
    if query:
        P
    
    return render(request, 'products/products.html')
