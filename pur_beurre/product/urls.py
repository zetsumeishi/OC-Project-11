from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("recherche/", views.search, name="search"),
]
