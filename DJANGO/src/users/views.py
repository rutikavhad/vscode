from django.shortcuts import redirect, render
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
#from django.views import View
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('home')
                
            else:
                messages.error(request, f'An error occured trying to login.')
        else:
            messages.error(request, f'An error occured trying to login.')
    elif request.method=='GET':

        login_from=AuthenticationForm()
    return render(request,'views/login.html',{'login_from':login_from})

# def register_view(request):
#     register_form=UserCreationForm()
#     return render(request,'views/register.html',{'register_form':register_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/home')

class RegisterView(View):

    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(
                request, f'User {user.username} registered successfully.')
            return redirect('home')
        else:
            messages.error(request, f'An error occured trying to register.')
            return render(request, 'views/register.html', {'register_form': register_form})



