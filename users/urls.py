from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("users_add/", users_add, name="users_add"),
    path("users_list/", users_list, name="users_list"),
    path("users_update/", users_update, name="users_update"),
    path("users_delete/", users_delete, name="users_delete"),
    path("generate_otp_for_user/",generate_otp_for_user, name ="generate_otp_for_user"),
    path("verify_otp/",verify_otp, name ="verify_otp"),
    path("logging_user/",logging_user, name ="logging_user"),
    path("user_logout/",user_logout, name ="user_logout"),
    path("reregister_user/",reregister_user, name ="reregister_user"),
    path("forget_password/",forget_password, name ="forget_password"),
    path("reset_password/",reset_password, name ="reset_password"),
]