from django.urls import path, include
from . import views

app_name="mainapp"
urlpatterns = [path("", views.landing_page, name="landing_page"),path("translator/", views.translator, name="translator"), path("review/", views.review, name="review"), path("users/<str:user_username>/", views.user_profile, name="user_profile"),path("decks/", views.decks, name="decks"), path("<str:deck_name>/", views.deck, name="deck"),
path("select2/", include("django_select2.urls")),
               ]