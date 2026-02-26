arr=[0,1,1]
count=0
for i in range(len(arr)-1):
    for j in range(i+1,len(arr)-1):
        for k in range(j+1,len(arr)-1):
            if arr[i]+arr[j]+arr[k] == 0:
                print(f"{arr[i]} + {arr[j] } + {arr[k]}")
                print(f"found {i} {j} {k} ",arr[i]+arr[j]+arr[k])