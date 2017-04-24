from django.test import TestCase
from django.contrib import auth

User=auth.get_user_model()

def user_login(self):
    user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
    self.client.force_login(user)
    return user

class LogoutViewTest(TestCase):

    def test_view_redirects_to_home(self):
        user=user_login(self)
        response=self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')
