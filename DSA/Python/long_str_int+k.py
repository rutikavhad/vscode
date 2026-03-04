#arr=[1,   2,  1,  1,  2,  2,  3,  2,  1,  3,  4,  2,  1,  3,  4,  4,  1,  3,  4,  1] 
arr=['A','B','A','A','B','B','C','B','A','C','D','B','A','C','D','D','A','C','D','A']
k=3


print(arr)
size=len(arr)
newa=[None]*size
t=k
count=1
s=0
for i in range(size):
    t=k
    for j in range(i+1,size+k):
        if t>0 and j<size:
            if arr[i]!=arr[j] :
                count+=1
                # print("count",count)
                t-=1
                # print("k",t)
            else:
                count+=1
                # print("count",count)
        elif t<=0 and j<size:
            if arr[i]==arr[j]:
                count+=1
                # print("count",count)
            else:
                newa[i]=count
                count=1
                break
        else:
            newa[i]=count
            count=1
            break
       



def max(new):
    max=0
    index=0
    for i in range(len(new)):
        if max<new[i]:
            index=i
            max=new[i]
        
    return max,index


def remax(old,k):
    a,b=max(newa)
    for i in range(b+1,a+b):
        if old[b] != old[i] and k>0:
            k-=1
            old[i]=old[b]

            

remax(arr,k)

#print(arr)
a,b=max(newa)
for i in range(b,a+1):
    print(arr[i])




