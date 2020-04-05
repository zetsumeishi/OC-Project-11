from django.test import TestCase
from django.contrib.auth import get_user_model


class AccountManagersTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.email = "olivier@gmail.com"
        self.password = "p455w0rd"
        self.first_name = "Olivier"

    def test_create_user(self):
        user = self.User.objects.create_user(
            self.email, self.first_name, password=self.password,
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
