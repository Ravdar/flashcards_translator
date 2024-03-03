from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name="users"
urlpatterns = [
    path("register/", views.register, name="register_view"),
    path("", include("django.contrib.auth.urls")),]