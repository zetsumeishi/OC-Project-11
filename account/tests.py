from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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


class AccountViewsTests(StaticLiveServerTestCase):
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
        response = self.client.post(reverse("account:signup"), data=form_data)
        self.assertRedirects(response, "/")
        response = self.client.get(reverse("account:signup"))
        self.assertEqual(
            list(response.context[-1]["form"].fields.keys()),
            ["email", "first_name", "password1", "password2"],
        )
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get(reverse("account:profile"))
        self.assertRedirects(
            response, "/mon-compte/connexion/?next=/mon-compte/"
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("account:profile"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_add_favorite(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("account:add_favorite"),
            {"product_id": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.favorites.all())
        self.client.logout()

    def test_remove_favorite(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("account:add_favorite"),
            {"product_id": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        response = self.client.get(
            reverse("account:remove_favorite"),
            {"product_id": 1},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.favorites.all())
        self.client.logout()

    def test_favorites(self):
        response = self.client.get(reverse("account:favorites"))
        self.assertRedirects(
            response, "/mon-compte/connexion/?next=/mon-compte/mes-favoris/"
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("account:favorites"))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_delete_account(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("account:delete_account"))
        self.assertRedirects(response, "/")
        qs = Account.objects.filter(email="olivier.loustaunau@gmail.com")
        self.assertFalse(qs)
        self.client.logout()

    def test_selenium_login(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-dev-shm-using")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--headless")
        self.selenium = webdriver.Chrome(
            executable_path=settings.CHROME_DRIVER,
            chrome_options=chrome_options,
        )
        self.selenium.implicitly_wait(10)
        url = self.live_server_url + reverse("account:login")
        self.selenium.get(url)
        self.selenium.find_element_by_id("id_username").send_keys(
            "olivier.loustaunau@gmail.com"
        )
        self.selenium.find_element_by_id("id_password").send_keys(
            "password" + Keys.RETURN
        )
        self.selenium.close()
