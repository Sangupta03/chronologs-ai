from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterTests(APITestCase):
    def setUp(self):
        cache.clear()  # avoid cross-test throttling on the shared "auth" scope

    def test_register_rejects_weak_password(self):
        res = self.client.post(
            "/api/auth/register/",
            {"email": "weak@example.com", "password": "password"},
        )
        self.assertEqual(res.status_code, 400)
        self.assertFalse(User.objects.filter(email="weak@example.com").exists())

    def test_register_accepts_strong_password(self):
        res = self.client.post(
            "/api/auth/register/",
            {"email": "strong@example.com", "password": "Str0ngPassword!9"},
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(email="strong@example.com").exists())


class LoginTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(email="login@example.com", password="Str0ngPassword!9")

    def test_login_with_correct_credentials_returns_tokens(self):
        res = self.client.post(
            "/api/auth/login/",
            {"email": "login@example.com", "password": "Str0ngPassword!9"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_with_wrong_password_is_rejected(self):
        res = self.client.post(
            "/api/auth/login/",
            {"email": "login@example.com", "password": "WrongPassword!9"},
        )
        self.assertEqual(res.status_code, 401)


class LogoutTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(email="logout@example.com", password="Str0ngPassword!9")
        login = self.client.post(
            "/api/auth/login/",
            {"email": "logout@example.com", "password": "Str0ngPassword!9"},
        )
        self.access = login.data["access"]
        self.refresh = login.data["refresh"]

    def test_logout_blacklists_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        res = self.client.post("/api/auth/logout/", {"refresh": self.refresh})
        self.assertEqual(res.status_code, 205)

        refresh_res = self.client.post("/api/auth/refresh/", {"refresh": self.refresh})
        self.assertEqual(refresh_res.status_code, 401)
