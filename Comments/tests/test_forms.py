from django.test import TestCase
from Comments.forms import CommentForm
from Comments.models import Comment
from django.contrib import auth

User=auth.get_user_model()

class CommentFormTests(TestCase):

    def test_form_default(self):
        form=CommentForm()
        self.assertIn("id_text", form.as_p())

    def test_form_save(self):
        user=User.objects.create_user(email="test@test.com", password="bla", first_name="Bla")
        form=CommentForm(data={'text': 'Bla'})
        self.assertTrue(form.is_valid())
        form.save(user)
        comment=Comment.objects.first()
        self.assertEqual(comment.text, "Bla")
        self.assertEqual(comment.author, user)
