from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'created_at',
        'status',
        'total_amount',
        'delivery_costs',
        'grand_total',
        'first_name',
        'last_name',
        'email',
    )

    list_filter = ('status', 'created_at')
    search_fields = (
        'order_number',
        'first_name',
        'last_name',
        'email',
    )

    readonly_fields = (
        'order_number',
        'created_at',
        'updated_at',
        'total_amount',
        'delivery_costs',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )
    inlines = (OrderItemInline,)

    ordering = ('-created_at',)

    fieldsets = (
        ('Order Info', {
            'fields': (
                'order_number',
                'status',
                'created_at',
                'updated_at',
                'stripe_pid',
                'original_bag',
            )
        }),
        ('Customer Info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone',
                'user',
                # 'profile',  # can cause logical crashs
            )
        }),
        ('Address', {
            'fields': (
                'address_line1',
                'address_line2',
                'city',
                'postal_code',
                'country',
            )
        }),
        ('Totals', {
            'fields': (
                'total_amount',
                'delivery_costs',
                'grand_total',
            )
        }),
    )