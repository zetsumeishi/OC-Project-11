from django.shortcuts import render

from product.forms import SearchForm


def home(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    context["jumbotron_search_form"] = SearchForm(auto_id="jumbotron_%s")
    return render(request, "www/home.html", context=context)


def legal_notice(request):
    context = {}
    context["search_form"] = SearchForm()
    return render(request, "www/legal-notice.html", context=context)
