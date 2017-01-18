from django.shortcuts import redirect, render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def add_sn(request):
    if request.method=='POST':
        return redirect('/1/', {'sn': request.POST['new_sn']})

def view_sn(request, sn):
    return render(request, 'sn.html', {'sn': sn})
