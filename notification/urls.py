from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("notification_add/", notification_add, name="notification_add"),
    path("notification_list/", notification_list, name="notification_list"),
    path("notification_update/", notification_update, name="notification_update"),
    path("notification_delete/", notification_delete, name="notification_delete"),
]