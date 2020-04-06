import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse

from .models import Product
from .forms import SearchForm


def search(request):
    context = {}
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data["product_name"]
            product = Product.objects.filter(product_name__iexact=product_name)
            if product:
                context["product"] = product[0]
                context["substitutes"] = product[0].find_substitute()
            return render(
                request, "product/search_results.html", context=context
            )
    return HttpResponseRedirect("/")


def autocomplete_product(request):
    if request.is_ajax():
        q = request.GET.get("term", "")
        search_qs = Product.objects.filter(product_name__istartswith=q)
        results = []
        for r in search_qs:
            results.append(r.product_name)
        data = json.dumps(results)
    else:
        data = "error"
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
