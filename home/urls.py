from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('privacy', views.privacy, name='privacy'),
    path('about', views.about, name='about'),
    path('impressum', views.impressum, name='impressum'),
    path('terms_conditions', views.terms_conditions, name='terms_conditions'),
]
