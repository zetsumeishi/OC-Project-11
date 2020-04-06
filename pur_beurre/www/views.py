from django.shortcuts import render

from product.forms import SearchForm


def home(request):
    context = {}
    context["search_form"] = SearchForm()
    return render(request, "www/home.html", context=context)
