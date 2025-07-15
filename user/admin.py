from django.contrib import admin
from .models import UserProfile, StyleProfile


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'street_address1',
        'town_or_city',
        'postcode',
        'country',
    )
    search_fields = (
        'user__username',
        'user__email',
        'phone_number',
        'street_address1',
        'town_or_city',
        'postcode',
    )
    list_filter = (
        'country',
    )


@admin.register(StyleProfile)
class StyleProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_profile',
        'jacket_size',
        'shirt_size',
        'trousers_size',
        'fit_preference',
        'preferred_color_1',
        'occasion_1',
    )
    search_fields = (
        'user_profile__user__username',
        'user_profile__user__email',
    )
    list_filter = (
        'fit_preference',
        'preferred_color_1',
        'preferred_color_2',
        'preferred_color_3',
        'occasion_1',
        'occasion_2',
        'occasion_3',
    )