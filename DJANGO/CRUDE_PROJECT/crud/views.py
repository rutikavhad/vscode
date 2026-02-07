from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product,User
from django.contrib.auth.decorators import login_required

# Create your views here. 
#this read data form db TEST   
@login_required 
def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})

#READ
@login_required
def read(request):
    user=User.objects.all()
    return render(request,'curd/read.html',{'user':user})


#CREATE NEW
@login_required
def create(request):
    if request.method=="POST":
        id=request.POST['id']
        name=request.POST['name']
        age=request.POST['age']

        User.objects.create(
            id=id,
            name=name,
            age=age
        )
        return redirect('read')
    return render(request,'curd/create.html')

#UPDATE DATA
@login_required
def update(request,id):
    user=User.objects.get(id=id)
    if request.method=="POST":
        user.name=request.POST['name']
        user.age=request.POST['age']
        user.save()
        return redirect('read')
    return render(request,'curd/update.html',{'user':user})

#DELETE
@login_required
def delete(request,id):
    user=User.objects.get(id=id)
    if request.method=="POST":
        user.id=request.POST['id']
        user.delete()
        return redirect('read')
    return render(request,'curd/delete.html',{'user':user})