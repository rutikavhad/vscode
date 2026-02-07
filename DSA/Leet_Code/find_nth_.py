#find n th index  element 
a1=2
a2=3
n=4 # find nth index elements

new=a2 #this used as add next data in last values
deff=a2-a1 
index=n-2  # we know first 2 index 
for i in range(index):
    new=new+deff
    #print(new)

print(new)