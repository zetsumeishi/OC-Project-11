from django.urls import path
from . import views

urlpatterns = [
    path("recherche/", views.search, name="search"),
    path(
        "ajax/recherche/",
        views.autocomplete_product,
        name="autocomplete_product",
    ),
]
