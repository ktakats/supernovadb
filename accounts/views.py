from django.shortcuts import redirect, reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def logout_view(request):
    logout(request)
    return redirect(reverse("home"))
