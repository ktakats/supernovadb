from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404, reverse

from models import SN, Project
from forms import NewSNForm, NewProjectForm
from accounts.forms import LoginForm
from Comments.forms import CommentForm

from astropy import units as u
from astropy.coordinates import SkyCoord

from django_tables2 import RequestConfig


User=auth.get_user_model()


def convert_coords_to_string(ra, dec):
    c=SkyCoord(str(ra), str(dec), unit=u.degree)
    ra='%02d:%02d:%02.3f' % (c.ra.hms.h, abs(c.ra.hms.m), abs(c.ra.hms.s))
    dec='{1:0{0}d}'.format(2 if c.dec.dms.d>=0 else 3, int(c.dec.dms.d))
    dec+=':%02d:%02.2f' % (abs(c.dec.dms.m), abs(c.dec.dms.s))
    return ra, dec

# Create your views here.
def home(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        email=request.POST['email']
        password=request.POST['password']
        if form.is_valid():
            user=authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('my_stuff'))
    else:
        form=LoginForm()
    return render(request, 'SNe/home.html', {'form': form})

@login_required(login_url='/')
def add_sn(request):
    if request.method=='POST':
        form=NewSNForm(data=request.POST, user=request.user)
        if form.is_valid():
            sn=form.save(request.user)
            return redirect(sn.get_absolute_url())
        else:
            return render(request, 'SNe/new_sn.html', {'form': form})
    else:
        form=NewSNForm(user=request.user)
        return render(request, 'SNe/new_sn.html', {'form':form})

@login_required(login_url='/')
def view_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    if request.method=="POST":
        commentform=CommentForm(request.POST)
        if commentform.is_valid():
            comment=commentform.save(request.user)
            sn.comments.add(comment)
            sn.save()
            return redirect(reverse('view_sn', args=(sn_id,)))
    ra, dec=convert_coords_to_string(sn.ra, sn.dec)
    projects=Project.objects.filter(sne=sn).exclude(archived=True)
    commentform=CommentForm()
    return render(request, 'SNe/sn.html', {'sn': sn, 'ra': ra, 'dec': dec, 'projects': projects, 'commentform': commentform})

@login_required(login_url='/')
def edit_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    if request.method=="POST":
        form=NewSNForm(data=request.POST, instance=sn)
        if form.is_valid():
            sn=form.save(request.user, sn_id)
            return redirect(sn.get_absolute_url())

    ra, dec=convert_coords_to_string(sn.ra, sn.dec)
    form=NewSNForm(instance=sn, initial={'ra': ra, 'dec': dec})
    return render(request, 'SNe/edit_sn.html', {'form': form})

@login_required(login_url='/')
def archive_sn(request, sn_id):
    sn=SN.objects.get(id=sn_id)
    sn.archived=True
    sn.save()
    return redirect(reverse('my_stuff'))

@login_required(login_url='/')
def my_stuff(request):
    sne=SN.objects.filter(Q(pi=request.user) | Q(coinvestigators=request.user)).exclude(archived=True).distinct()
    projects=Project.objects.filter(Q(pi=request.user) | Q(coinvestigators=request.user)).exclude(archived=True).distinct()
    return render(request, 'SNe/my_stuff.html', {'sne': sne, 'projects': projects})

@login_required(login_url="/")
def add_project(request):
    if request.method=="POST":
        form=NewProjectForm(request.POST, user=request.user)
        if form.is_valid():
            project=form.save(request.user)
            return redirect(project.get_absolute_url())
    form=NewProjectForm(user=request.user)
    return render(request, 'SNe/new_project.html', {'form': form})

@login_required(login_url="/")
def view_project(request, project_id):
    project=Project.objects.get(id=project_id)
    if request.method=="POST":
        commentform=CommentForm(request.POST)
        if commentform.is_valid():
            comment=commentform.save(request.user)
            project.comments.add(comment)
            project.save()
            return redirect(reverse('view_project', args=(project_id,)))
    commentform=CommentForm()
    return render(request, 'SNe/project.html', {'project': project, 'commentform': commentform})

@login_required(login_url="/")
def edit_project(request, project_id):
    project=Project.objects.get(id=project_id)
    if request.method=="POST":
        form=NewProjectForm(request.POST, instance=project)
        if form.is_valid():
            project=form.save(request.user, project_id)
            return redirect(project.get_absolute_url())
    form=NewProjectForm(instance=project)
    return render(request, 'SNe/edit_project.html', {'form': form})

@login_required(login_url='/')
def archive_project(request, project_id):
    project=Project.objects.get(id=project_id)
    project.archived=True
    project.save()
    return redirect(reverse('my_stuff'))