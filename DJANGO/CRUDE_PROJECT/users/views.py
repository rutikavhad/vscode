from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

from .models import Profile
from .forms import user_reg


def user_signup(request):
    if request.method=="POST":
        form=user_reg(request.POST)
        if form.is_valid():
            user=User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']

            )
        profile=Profile.objects.create(
            user=user,
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            phone=request.POST.get('phone')
        )
        return redirect('login')
    else:
        form=user_reg()
    return render(request,'register.html',{'form':form})



def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['pass']

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('read')
        else:
            messages.error(request,'invalid info')

    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')