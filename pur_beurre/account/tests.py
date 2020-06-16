from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from django.test.client import Client
from django.urls import reverse

from .models import Account
from product.models import Product


class AccountManagersTests(TestCase):
    fixtures = ["accounts.json"]

    def setUp(self):
        self.User = get_user_model()
        self.email = "olivier@gmail.com"
        self.password = "p455w0rd"
        self.first_name = "Olivier"

    def test_create_user(self):
        user = self.User.objects.create_user(
            self.email, self.first_name, password=self.password,
        )
        with self.assertRaises(ValueError):
            user = self.User.objects.create_user(
                None, self.first_name, password=self.password,
            )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = self.User.objects.create_superuser(
            self.email, self.first_name, password=self.password
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)


class AccountModelsTests(TestCase):
    fixtures = ["accounts.json", "products.json"]

    def setUp(self):
        self.user = Account.objects.get(email="olivier.loustaunau@gmail.com")
        self.user.favorites.add(Product.objects.get(pk=1))

    def test_models_methods(self):
        self.assertEqual(self.user.__str__(), "olivier.loustaunau@gmail.com")
        self.assertTrue(self.user.has_perm("account.profile"))
        self.assertTrue(self.user.has_module_perms("product"))
        self.assertTrue(self.user.get_favorites())


class AccountViewsTests(LiveServerTestCase):
    fixtures = ["accounts.json", "products.json"]

    def setUp(self):
        self.user = Account.objects.get(email="olivier.loustaunau@gmail.com")
        self.user.favorites.add(Product.objects.get(pk=1))
        self.client = Client()

    def test_signup(self):
        form_data = {
            "email": "new_user@example.com",
            "password1": "password",
            "password2": "password",
            "first_name": "user",
        }
        response = self.client.post(reverse("signup"), data=form_data)
        self.assertRedirects(response, "/")
        response = self.client.get(reverse("signup"))
        self.assertEqual(
            list(response.context[-1]["form"].fields.keys()),
            ["email", "first_name", "password1", "password2"],
        )
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/account/connexion/?next=/account/")
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_favorites(self):
        response = self.client.get(reverse("favorites"))
        self.assertRedirects(
            response, "/account/connexion/?next=/account/mes-favoris/"
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_add_favorite(self):
        pass

    def test_remove_favorite(self):
        pass

    def test_delete_account(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_account"))
        self.assertRedirects(response, "/")
        qs = Account.objects.filter(email="olivier.loustaunau@gmail.com")
        self.assertFalse(qs)
