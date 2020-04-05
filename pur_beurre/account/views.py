from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)

from .models import Account
from .forms import AccountCreationForm, SigninForm


def signup(request):
    context = {}
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            Account.objects.create_user(email, first_name, password=password)
            user = authenticate(email=email, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        context["form"] = AccountCreationForm()
        return render(request, "account/signup.html", context=context)


@login_required
def profile(request):
    context = {}
    context["password_form"] = PasswordChangeForm(request.user)
    return render(request, "account/profile.html", context=context)


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return HttpResponseRedirect("/")
