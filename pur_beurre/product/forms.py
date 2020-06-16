from django import forms


class SearchForm(forms.Form):
    product_name = forms.CharField(max_length=100)
