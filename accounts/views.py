from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse

# Create your views here.

def logIn(request):
    email=request.POST['email']
    password=request.POST['password']
    user=authenticate(username=email, password=password)
    if user:
        login(request, user)
    return redirect(reverse('home'))
