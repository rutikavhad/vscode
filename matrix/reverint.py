num=1534236469
temp=num


sign=-1 if num <0 else 1
temp=abs(num)
arr=[]
while temp>0:
    arr.insert(100,temp%10)
    temp//=10
    print(arr)

result=0

for i in arr:
    result=result*10+i
result*=sign
print(result)