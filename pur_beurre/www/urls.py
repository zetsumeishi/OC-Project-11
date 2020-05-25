from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mentions-legales/", views.legal_notice, name="legal-notice"),
]
