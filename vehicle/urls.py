from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("vehicle_add/", vehicle_add, name="vehicle_add"),
    path("vehicle_list/", vehicle_list, name="vehicle_list"),
    path("vehicle_update/", vehicle_update, name="vehicle_update"),
    path("vehicle_delete/", vehicle_delete, name="vehicle_delete"),
]