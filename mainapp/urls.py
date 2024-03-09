from django.urls import path
from . import views

app_name="mainapp"
urlpatterns = [path("", views.landing_page, name="landing_page"),path("translator/", views.translator, name="translator"), path("review/", views.review, name="review"), path("users/<str:user_username>/", views.user_profile, name="user_profile")
               ]