from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="business_center"),
    path("management/", views.product_management, name="bc_product_management"),
    path("variant/<int:pk>/plus/", views.variant_plus, name="bc_variant_plus"),
    path("variant/<int:pk>/minus/", views.variant_minus, name="bc_variant_minus"),
    path("variant/<int:pk>/duplicate/",
         views.variant_duplicate, name="bc_variant_duplicate"),
    path("variant/<int:pk>/remove/",
         views.variant_remove, name="bc_variant_remove"),
    path("variant/<int:pk>/edit/", views.variant_edit, name="bc_variant_edit"),
    path("variant/create/", views.variant_create, name="bc_variant_create"),
    path("user-rights/", views.user_rights, name="user_rights"),
    path("user-rights/<int:pk>/toggle/", views.user_rights_toggle, name="user_rights_toggle"),
]
