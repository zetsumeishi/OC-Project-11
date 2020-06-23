from django.shortcuts import render, HttpResponseRedirect

from .models import Product
from .forms import SearchForm


def search(request):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]
            product = Product.objects.filter(
                product_name__icontains=product_name
            )
            if product:
                context["product"] = product[0]
                context["substitutes"] = product[0].find_substitute()
            return render(
                request, "product/search_results.html", context=context
            )
    return HttpResponseRedirect("/")


def single(request, product_name):
    context = {}
    context["nav_search_form"] = SearchForm(auto_id="nav_%s")
    context["product"] = Product.objects.filter(
        product_name__iexact=product_name
    )[0]
    return render(request, "product/single.html", context=context)
