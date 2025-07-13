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


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delet=models.PROTECT)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    occasion = models.CharField(max_length=50, blank=True)
    collection_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

