from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "rating",
        "created_at",
    )
    list_filter = (
        "rating",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "product__name",
        "comment",
    )
    ordering = ("-created_at",)