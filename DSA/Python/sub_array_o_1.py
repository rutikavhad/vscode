arr=[1,0,1,0,3,0,7,5,1,1,1,9,8,0,8,1,5,1,1,5,7,9,1,0,0,0,0,0,1,1,]
count=0
old=0
for i in range(len(arr)):
    if arr[i]==1 or arr[i]==0:
        count+=1
    else:
        if old<count:
            old=count
            count=0
        else:
            count=0

print(old)
print(count)
