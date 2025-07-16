from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('order/<int:order_id>', views.order_details, name='order_details'),
    path('manage_appointments', views.manage_appointments, name="manage_appointments"),
    path('edit_appointment/<int:appt_id>', views.edit_appointment, name="edit_appointment"),
    path("delete_appointment/<int:appt_id>/", views.delete_appointment, name="delete_appointment"),
    path("edit_review/<int:product_id>/", views.edit_review, name="edit_review"),
]
