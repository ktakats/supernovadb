from django.contrib.auth.backends import ModelBackend
from django.contrib import auth

User=auth.get_user_model()

class EmailAuthenticationBackend(ModelBackend):

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email__iexact = email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
