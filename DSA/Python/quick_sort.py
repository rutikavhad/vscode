arr=[1,5,4,6,9,7,3,2,8]

# def swap(arr,i,j):
#     temp=arr[i]
#     arr[i]=arr[j]
#     arr[j]=temp
count=0





def quicksort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p - 1)
        quicksort(arr, p + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1



quicksort(arr,0,len(arr)-1)


#this not quick sort normal sort
for i in range(len(arr)):
    for j in range(len(arr)-1,i,-1):
        count+=1
        if arr[i]>arr[j]:
            swap(arr,i,j)
            

print(arr)
print(f"array size is{len(arr)} count is {count}")
