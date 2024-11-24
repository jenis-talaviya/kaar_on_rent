from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('payments/', payment_page, name='payment_page'),
    path("payment_add/", payment_add, name="payment_add"),
    path("payment_verify/", payment_verify, name="payment_verify"),
    path("payment_list/", payment_list, name="payment_list"),
    path("payment_update/", payment_update, name="payment_update"),
    path("payment_delete/", payment_delete, name="payment_delete"),
]