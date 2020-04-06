from django import forms

from .models import Product


class SearchForm(forms.Form):
    product_name = forms.CharField(max_length=100)
