from django.contrib import admin
from .models import Product, Category, Occasion, Series, Size, Fit, Color, ProductVariant


# Register your models here.
admin.site.register(Category)
admin.site.register(Occasion)
admin.site.register(Series)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Fit)
admin.site.register(Color)
admin.site.register(ProductVariant)