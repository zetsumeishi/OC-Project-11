from django.test import TestCase
from django.test.client import Client
import json
from django.urls import reverse


class WwwViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_legal_notice(self):
        response = self.client.get(reverse("legal-notice"))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
