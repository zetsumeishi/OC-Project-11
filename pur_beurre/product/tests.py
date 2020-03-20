from django.test import TestCase

from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product_data = {
            "product_name": "Nutella",
            "url": "https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero",
            "image_url": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.168.400.jpg",
            "nutriscore_grade": "e",
            "nova_group": "4",
            "fat_100g": "30.9",
            "saturated_fat_100g": "10.6",
            "sugars_100g": "56.3",
            "salt_100g": "0.107",
        }
        self.product = Product(**self.product_data)

    def test_product_instance(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(str(self.product), self.product_data["product_name"])

    def tearDown(self):
        pass
