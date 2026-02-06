arr=[4,5,3,1,2]

#for i in range(0,10,2) for(i=0;i<10;i+=2) op:-  0, 2, 4, 6, 8

# for i in range(20,10,-2) for(i=20;i>10;i-=2):-20, 18, 16, 14, 12


for i  in range (len(arr)-1):
    for j in range(i+1,0,-1):  #for(j=i+1,j>0;j--)
        if arr[j]<arr[j-1]:
            temp=arr[j]
            arr[j]=arr[j-1]
            arr[j-1]=temp
        else:
            break

print(arr)

# for i in range(10):
#     for j in range(i+1,0,-1):
#         print(j)