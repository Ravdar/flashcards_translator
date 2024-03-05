from django.urls import path
from . import views

app_name="mainapp"
urlpatterns = [path("", views.landing_page, name="landing_page"),path("translator/", views.translator, name="translator")
               ]