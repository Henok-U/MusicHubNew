from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCustomManager(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user@email.com",
            password="23#43_34dfa",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.email, "user@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

    def test_create_superuser(self):
        User = get_user_model()
        super_user = User.objects.create_superuser(
            email="admin@email.com",
            password="23#43_3)4dfa",
            first_name="Admin John",
            last_name="testDoe",
        )
        self.assertEqual(super_user.email, "admin@email.com")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_admin)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

        try:
            self.assertIsNone(super_user.username)
        except AttributeError:
            pass
