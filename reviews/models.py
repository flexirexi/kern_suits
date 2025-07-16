from django.db import models
from django.conf import settings
from products.models import Product


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.FloatField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # only one review per user and product..

    def __str__(self):
        first_name = self.user.first_name or ""
        last_name_cropped = (self.user.last_name[:1] + ".") if self.user.last_name_cropped else ""
        return f"Review by {first_name} {last_name_cropped} for {self.product}"