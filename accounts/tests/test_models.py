from django.test import TestCase
from django.contrib import auth

User=auth.get_user_model()

class UserModelTest(TestCase):

    def test_can_create_user(self):
        User.objects.create(email="test@test.com", password="bla")
        self.assertEqual(User.objects.count(),1)
