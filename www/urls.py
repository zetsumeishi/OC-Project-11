from django.urls import path

from . import views

app_name = "www"

urlpatterns = [
    path("", views.home, name="home"),
    path("mentions-legales/", views.legal_notice, name="legal-notice"),
    path("mail-envoye/", views.send_email, name="send-email"),
]
