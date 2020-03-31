from django.forms import ModelForm
from .models import Product


class ArticleForm(ModelForm):
    class Meta:
        model = Product
        fields = ["product_name"]
