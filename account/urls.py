from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "account"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("inscription/", views.signup, name="signup"),
    path("mes-favoris/", views.favorites, name="favorites"),
    path("ajax/ajout-favoris/", views.add_favorite, name="add_favorite",),
    path("retirer-favori/", views.remove_favorite, name="remove_favorite"),
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
            template_name="account/password_change.html", success_url="/",
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
]
