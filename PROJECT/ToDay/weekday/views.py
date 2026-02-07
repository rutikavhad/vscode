from django.shortcuts import render
from .services.calnder import fullday
# Create your views here.

def displydate(request):
    result=None
    if request.method=="POST":
        dd=str(request.POST.get("dd"))
        mm=str(request.POST.get("mm"))
        yy=str(request.POST.get("yyyy"))
        print(yy,mm,dd)

        result=fullday(yy,mm,dd)
        print(result)
        #fullday('2003','09','09') #give input as sting not number 0 not inital work

    return render(request,'index.html',{'result':result})
