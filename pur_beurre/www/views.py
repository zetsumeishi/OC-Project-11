from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "www/home.html", context=context)
