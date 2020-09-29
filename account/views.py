from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
)

from .models import Account
from .forms import AccountCreationForm
from product.models import Product
from product.forms import SearchForm


def ajax_is_authenticated(request):
    if request.user.is_authenticated:
        return {"authenticated": True}
    else:
        return {"authenticated": False}


def signup(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
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
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    context["password_form"] = PasswordChangeForm(request.user)
    return render(request, "account/profile.html", context=context)


@login_required
def favorites(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    user = request.user
    context["favorites"] = user.get_favorites()
    return render(request, "account/favorites.html", context=context)


def add_favorite(request):
    if request.is_ajax():
        response = ajax_is_authenticated(request)
        if not response["authenticated"]:
            return JsonResponse(response, status=403)
        user = request.user
        product_id = request.GET.get("product_id", "")
        product = Product.objects.get(pk=int(product_id))
        user.favorites.add(product)
        return JsonResponse(response, status=200)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_favorite(request):
    if request.is_ajax():
        response = ajax_is_authenticated(request)
        if not response["authenticated"]:
            return JsonResponse(response, status=403)
        user = request.user
        product_id = request.GET.get("product_id", "")
        product = Product.objects.get(pk=int(product_id))
        user.favorites.remove(product)
        response.update({"id": str(product_id)})
        return JsonResponse(response, status=200)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return HttpResponseRedirect("/")
