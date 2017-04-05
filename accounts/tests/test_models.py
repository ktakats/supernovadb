from django.test import TestCase
from django.contrib import auth

User=auth.get_user_model()

class UserModelTest(TestCase):

    def test_can_create_user(self):
        User.objects.create_user(email="test@test.com", password="bla", first_name="Test")
        self.assertEqual(User.objects.count(),1)

    def test_can_create_two_users(self):
        User.objects.create_user(email="test@test.com", password="bla", first_name="test")
        User.objects.create_user(email="bla@test.com", password="bla", first_name="Bla")
        self.assertEqual(User.objects.count(), 2)
