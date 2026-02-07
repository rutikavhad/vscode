
def tribi(n):
    f1=0
    f2=1
    f3=2
    f4=0
    for i in range(n):
        f4=f1+f2+f3
        f1=f2
        f2=f3
        f3=f4
        i+=1
    print(f4)






