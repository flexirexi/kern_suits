from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_bag, name='bag'),
    path("add/", views.add_to_bag, name="add_to_bag"),
    path("update/<int:variant_id>/", views.update_bag, name="update_bag"),
    path("remove/<int:variant_id>/", views.remove_from_bag, name="remove_from_bag"),
]