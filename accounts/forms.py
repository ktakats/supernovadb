from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate

User=auth.get_user_model()

class LoginForm(forms.models.ModelForm):

    class Meta:
        model=User
        fields=['username', 'password']
        labels={
            'username': 'Email'
        }
        widgets={
            'password': forms.PasswordInput()
        }
        error_messages={
            'username': {'required': 'Please provide your email address'}
        }


    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        user=authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError('Login is invalid. Please try again.')
        return self.cleaned_data
