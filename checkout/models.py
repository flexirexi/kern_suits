from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
import uuid
from decimal import Decimal

from products.models import ProductVariant
# from user.models import UserProfile  # not yet created but i had issue in the last project changing models, so I do it now


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    # profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = CountryField(blank_label='Country *', null=False, blank=False)

    # Financial fields
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Stripe PaymentIntent ID
    stripe_pid = models.CharField(max_length=255, blank=True, null=True)

    # Original cart -> is easier for later
    original_bag = models.TextField(blank=True, null=True)

    def update_total(self):
        """ Updates the total amount and grand total """
        self.total_amount = sum(
            item.price * item.quantity for item in self.items.all()
        )
        self.grand_total = Decimal(str(self.total_amount)) + Decimal(str(self.delivery_costs))
        self.save()

    def save(self, *args, **kwargs):
        """"""
        # Generate order number if missing
        if not self.order_number:
            self.order_number = uuid.uuid4().hex.upper()
        # Ensure grand total is always up to date
        self.grand_total = (self.total_amount or 0) + (self.delivery_costs or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} * {self.variant}"
    