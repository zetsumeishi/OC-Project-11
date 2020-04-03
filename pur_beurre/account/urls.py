from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("inscription/", views.signup, name="signup"),
    path("supprimer-mon-compte/", views.delete_account, name="delete_account"),
    path(
        "connexion/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path(
        "deconnexion/",
        auth_views.LogoutView.as_view(template_name="account/logged_out.html"),
        name="logout",
    ),
    path(
        "changer-mot-de-passe/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "mot-de-passe-change/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "reinitialiser-mot-de-passe/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "mot-de-passe-reinitialise/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "confirmation-reinitialisation/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reinitialisation-terminee/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
