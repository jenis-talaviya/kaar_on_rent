from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("vehiclemaintaine_add/", vehiclemaintaine_add, name="vehiclemaintaine_add"),
    path("vehiclemaintaine_list/", vehiclemaintaine_list, name="vehiclemaintaine_list"),
    path("vehiclemaintaine_update/", vehiclemaintaine_update, name="vehiclemaintaine_update"),
    path("vehiclemaintaine_delete/", vehiclemaintaine_delete, name="vehiclemaintaine_delete"),
]