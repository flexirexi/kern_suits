from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('order/<int:order_id>', views.order_details, name='order_details'),
    path('manage_appointments', views.manage_appointments, name="manage_appointments"),
]
