from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("booking_add/", booking_add, name="booking_add"),
    path("booking_list/", booking_list, name="booking_list"),
    path("booking_update/", booking_update, name="booking_update"),
    path("booking_delete/", booking_delete, name="booking_delete"),
]