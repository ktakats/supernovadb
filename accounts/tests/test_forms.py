from django.test import TestCase
from accounts.forms import LoginForm

class LoginFormTest(TestCase):

    def test_default(self):
        form=LoginForm()
        self.assertIn('Email', form.as_p())

    def test_form_validation_for_blank_items(self):
        form=LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Please provide your email address'])

    def test_user_must_exist(self):
        form=LoginForm(data={'username': 'test@test.com', 'password': 'bla'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ['Login is invalid. Please try again.'])
