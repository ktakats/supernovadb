from django.test import TestCase
from django.contrib import auth
from Comments.models import Comment

User=auth.get_user_model()

class CommentViewTests(TestCase):

    def test_view_renders_template(self):
        response=self.client.get('/comments/')
        self.assertTemplateUsed(response, 'Comments/comments.html')

    def test_view_shows_comments(self):
        user=User.objects.create_user(email="test@test.com", password="bla", first_name="Bla")
        comment=Comment.objects.create(text="Test", author=user)
        response=self.client.get('/comments/')
        self.assertContains(response, comment.text)
        self.assertContains(response, comment.author)
        self.assertContains(response, "2017")
