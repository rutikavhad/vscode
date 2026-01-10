from django.shortcuts import redirect, render
from django.shortcuts import render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login

def login_view(request):
    if request.method=='POST':
        login_from=AuthenticationForm(request=request,data=request.POST)
        if login_from.is_valid():
            username=login_from.cleaned_data.get('username')
            password=login_from.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('home')
                
            else:
                pass
    elif request.method=='GET':

        login_from=AuthenticationForm()
    return render(request,'views/login.html',{'login_from':login_from})
