from django.shortcuts import render, redirect
from Comments.models import Comment

# Create your views here.

def comment(request):
    comments=Comment.objects.all()
    return render(request, 'Comments/comments.html', {'comments': comments})
