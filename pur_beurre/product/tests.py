import os

from django.test import TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client
from django.urls import reverse

from selenium import webdriver

from .models import Product
from .forms import SearchForm


class ProductModelsTests(LiveServerTestCase):
    fixtures = ["products.json"]

    def setUp(self):
        self.product_data = {
            "product_name": "Ferrero Rocher",
            "url": "https://fr.openfoodfacts.org/produit/4008400163826",
            "image_url": "https://static.openfoodfacts.org/images/products/400/840/016/3826/front_de.8.400.jpg",  # NOQA
            "nova_group": "4",
            "nutriscore_grade": "e",
            "saturated_fat_100g": 14.100,
            "fat_100g": 42.700,
            "salt_100g": 0.153,
            "sugars_100g": 39.900,
            "category": "bonbons",
        }
        self.product = Product(**self.product_data)

    def test_product_instance(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(str(self.product), self.product_data["product_name"])

    def test_find_substitute(self):
        self.assertTrue(self.product.find_substitute())

    def tearDown(self):
        pass


class ProductFormsTests(TestCase):
    def test_forms(self):
        form_data = {"product_name": "Ferrero Rocher"}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        form_data = {"product_name": ""}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProductViewsTests(StaticLiveServerTestCase):
    fixtures = ["products.json"]

    def setUp(self):
        self.search_term = "Milka"
        self.client = Client()
        self.selenium = webdriver.Chrome(os.environ.get("CHROME_DRIVER"))
        self.selenium.implicitly_wait(10)
        self.selenium.set_window_position(0, 0)
        self.selenium.set_window_size(1280, 960)

    def test_search(self):
        response = self.client.post(
            reverse("search"), data={"product_name": "Ferrero Rocher"}
        )
        self.assertEqual(response.status_code, 200)

    def test_autocomplete_product(self):
        self.selenium.get(self.live_server_url)
        product_input = self.selenium.find_element_by_id("id_product_name")
        product_input.send_keys(self.search_term)
        product_input.send_keys(" ")
        self.assertTrue(
            self.selenium.find_element_by_xpath('//*[@id="ui-id-1"]')
        )
