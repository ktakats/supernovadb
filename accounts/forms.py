from django import forms
from django.contrib import auth

User=auth.get_user_model()

class LoginForm(forms.models.ModelForm):

    class Meta:
        model=User
        fields=['username', 'password']
        labels={
            'username': 'Email'
        }
        error_messages={
            'username': {'required': 'Please provide your email address'}
        }
