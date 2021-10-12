from django.test import TestCase

from .models import User


class UserTesteCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user("cfe", password="abc123")

    def test_user_pw(self):
        checked = self.user_a.check_password("abc123")
        self.assertTrue(checked)


class UserRecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user("cfe", password="abc123")

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)
