from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)


class Series(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class Occasion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    occasion = models.ForeignKey(Occasion, related_name="products", on_delete=models.PROTECT)
    series = models.ForeignKey(Series, related_name="products", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    fabric = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)
    kind = models.CharField(max_length=20)


class Fit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)


class Color(models.Model):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    hex_code = models.CharField(max_length=20)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    fit = models.ForeignKey(Fit, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

