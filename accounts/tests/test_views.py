from django.test import TestCase
from django.contrib import auth

User=auth.get_user_model()

class LoginViewTest(TestCase):

    def test_user_can_log_in(self):
        User.objects.create_user(username="test@test.com", password="blabla")
        response=self.client.post('/accounts/login/', {'email': 'test@test.com', 'password': 'blabla'})
        user=auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
