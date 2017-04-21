from django.test import TestCase
from Comments.models import Comment
from SNe.models import SN
from datetime import datetime
from django.contrib import auth

User=auth.get_user_model()

class CommentModelTest(TestCase):

    def test_can_create_comments(self):
        comment=Comment()
        self.assertEqual(comment.text, "")

    def test_model_sets_author(self):
        user=User.objects.create(email="test@test.com", password="bla", first_name="Bla")
        t=datetime.now()
        comment=Comment.objects.create(text="bla", author=user)
        self.assertEqual(comment.author, user)
