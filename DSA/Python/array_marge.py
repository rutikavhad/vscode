a1=[1,3,4,7,0,0,0,0]
a2=[2,5,6,8]

n=len(a1)-1
m1=m2=len(a2)-1

# print(a1[m1],a2[m2])
for i in range(len(a1)-1):
    if a1[m1] < a2[m2]:
        a1[n]=a2[m2]
        m2-=1
        n-=1
        print(a1)
        print(a2)
        #print("m2 is",m2)
        #print("n is ",n)
    else:
        temp=a1[m1]
        a1[m1]=a1[n]
        a1[n]=temp
        m1-=1
        n-=1
        print(a1)
        #print("m1 is ",m1)



