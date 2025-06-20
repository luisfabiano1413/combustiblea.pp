# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar-vehiculo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('mis-vehiculos/', views.mis_vehiculos, name='mis_vehiculos'),
    
]