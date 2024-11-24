from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("invoice_add/", invoice_add, name="invoice_add"),
    path("invoice_list/", invoice_list, name="invoice_list"),
    path("invoice_update/", invoice_update, name="invoice_update"),
    path("invoice_delete/", invoice_delete, name="invoice_delete"),
]