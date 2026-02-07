arr=[1,3,7,5,6,2,0,8,9,7,11]

target=6
size=len(arr)
for i in range(size):
    if arr[i]==target:
        index=i
        #print(arr[i])
        for j in range(i,size):
            if arr[j]>arr[index]:
                upless=arr[j]
                for k in range(j,size):
                    if upless >arr[k]:
                        upless=arr[k]
                        print(f"upless{upless}")
                    else:
                        print(upless)
                break

