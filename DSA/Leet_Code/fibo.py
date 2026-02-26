old=0
new=1
def fibo(old ,new):
    if new+old>155:
        return
    print(new+old)
    temp=new+old
    old=new
    new=temp
    fibo(old,new)



a=5
b=12

a=a+b
b=a-b
a=a-b

print(a,b)