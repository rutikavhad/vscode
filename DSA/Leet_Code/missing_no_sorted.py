arr=[1,3,4,5,7,8,9,10,12,13] #2,6,11 are missing

# arr1=[3,4,5,8,9,10,11] #6,7 are missing
# length1=len(arr1)
# print(f"total missing is {(arr1[length1-1]-length1)-(arr1[0]-1)}") # this print if number not start from index 0 as 1 

length=len(arr)
print(f"total missing {(arr[length-1]-length)-(arr[0]-1)}") 
# print(length)
less=arr[0]
for  i in range(length):
    if arr[i]!=(less+i+1):
        print(less+i)