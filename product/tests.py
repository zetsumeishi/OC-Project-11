from django.test.client import Client
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase

from .models import Product
from .forms import SearchForm


class ProductModelsTests(LiveServerTestCase):
    fixtures = ["products.json"]

    def setUp(self):
        self.product_data = {
            "id": 8,
            "product_name": "Ferrero Rocher",
            "url": "https://fr.openfoodfacts.org/produit/4008400163826",
            "image_url": "https://static.openfoodfacts.org/images/products/400/840/016/3826/front_de.8.400.jpg",  # NOQA
            "nova_group": "4",
            "nutriscore_grade": "e",
            "saturated_fat_100g": 14.100,
            "fat_100g": 42.700,
            "salt_100g": 0.153,
            "sugars_100g": 39.900,
        }
        self.product = Product(**self.product_data)

    def test_product_instance(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(str(self.product), self.product_data["product_name"])

    def test_find_substitute(self):
        self.assertFalse(self.product.find_substitute())

    def tearDown(self):
        pass


class ProductFormsTests(TestCase):
    def test_forms(self):
        form_data = {"product_name": "duette vanille"}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        form_data = {"product_name": ""}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProductViewsTests(LiveServerTestCase):
    fixtures = ["products.json"]

    def setUp(self):
        self.search_term = "duette vanille"
        self.client = Client()

    def test_search(self):
        response = self.client.get(reverse("product:search"))
        self.assertRedirects(response, "/")
        response = self.client.post(
            reverse("product:search"),
            {"product_name": self.search_term},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["substitutes"])
