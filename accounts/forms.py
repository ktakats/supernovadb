from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate

User=auth.get_user_model()

class LoginForm(forms.models.ModelForm):

    class Meta:
        model=User
        fields=['email', 'password']

        widgets={
            'password': forms.PasswordInput()
        }
        error_messages={
            'email': {'required': 'Please provide your email address'}
        }

        labels={
            'email': "Email"
        }


    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        user=authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError('Login is invalid. Please try again.')
        return self.cleaned_data
