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
