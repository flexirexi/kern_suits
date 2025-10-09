from django.urls import path
from . import views

app_name = "business_center"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]