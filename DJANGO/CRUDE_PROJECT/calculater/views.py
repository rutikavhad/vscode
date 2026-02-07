from django.shortcuts import render
from .services.cal import add,divide,subtract,multiply,kaprekar


# Create your views here.

def  calcu(request):
    result=None
    if request.method=="POST":
        a=int(request.POST.get("a")) # type must be same from (FORM)   POST remove error
        b=int(request.POST.get("b"))
        operation=request.POST.get('operation') #+-*/ selecter
        if operation=="add":
            result=add(a,b)
        elif operation=="sub":
            result=subtract(a,b)
        elif operation=="mul":
            result=multiply(a,b)
        elif operation=="div":
            result=divide(a,b)
    return render(request,'calculater.html',{'result':result})

def kalp(request):
    output=None
    if request.method=="POST":
        num_str=request.POST.get("num")
        output=kaprekar(num_str)
    return render(request,'calculater.html',{'output':output})



#learn froms.py 

from .forms import contactform

def contects(request):
   # form=contactform
    if request.method=="POST":
        form=contactform(request.POST)
        if form.is_valid:
            # name=form.cleaned_data['name']
            # email=form.cleaned_data['email']
            # message=form.cleaned_data['message']

            form.save()
    else:
        form=contactform()


            #test sample
            # print(name,email,message)

    return render(request,'index.html',{'form':form})
