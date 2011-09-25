# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from members.forms import RegistrationForm, ProfileForm
from members.models import *
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.core import serializers
import re

##############################
# Member views
##############################

# Registration page
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            #Generate a username and create user
            username=generate_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
            new_user=User.objects.create_user(username, form.cleaned_data['email'], form.cleaned_data['password1'])
            new_user.first_name=form.cleaned_data['first_name']
            new_user.last_name=form.cleaned_data['last_name']
            new_user.save()
            return redirect('/')
    else:
        form=RegistrationForm()
    return render(request,'auth/registration_form.html',{'form':form})

# Edit Profile Page
@login_required
def edit_profile(request):
    profile=request.user.get_profile()
    if request.method=='POST':
        form=ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/member/home/')
    else:
        form=ProfileForm(instance=profile)
    return render(request,'members/edit_profile.html',{'form':form,'profile':profile})

# Upload Photo Page
@login_required    
def upload_photo(request):
    profile=request.user.get_profile()
    if request.method=='POST':
        form=PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            newphoto=form.save()
            profile.photos.add(newphoto)
            if profile.mainphoto is None:
                profile.mainphoto=newphoto
                profile.points+=5
                profile.save()
            return redirect('/member/home/')
    else:
        form=PhotoForm()
    return render(request,'members/upload_photo.html',{'form':form})
 

##############################
# AJAX Views
##############################

@login_required
def add_follower(request,member_id):
    profile=request.user.get_profile()
    try:
        u=User.objects.get(username__exact=member_id).get_profile()
    except User.DoesNotExist:
        return HttpResponse('Invalid User')
    profile.follows.add(u)
    profile.points+=1
    profile.save()
    u.points+=5
    u.save()
    return HttpResponse('Follower Added')

@login_required
def remove_follower(request,member_id):
    profile=request.user.get_profile()
    try:
        u=User.objects.get(username__exact=member_id).get_profile()
    except User.DoesNotExist:
        return HttpResponse('Invalid User')
    profile.follows.remove(u)
    return HttpResponse('Follower Removed')
    
##############################
# Misc Functions
##############################

### Generate username ###
def generate_username(first_name, last_name):
    username=first_name+last_name
    re.sub(r'\W+','',username)
    i=0
    baseusername=username
    while User.objects.filter(username__exact=username):
        i+=1
        username = "%s%d" % (baseusername, i)
    return username
