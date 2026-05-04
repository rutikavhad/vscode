def graphs(arr,node1,node2,weight):
    #print(arr[node1][node2])
    print(node1)
    print(node2)
    print(weight)
    arr[node1][node2]=weight




def disp(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            print(f"index {i} index {j} values is {arr[i][j]}")



vir=int(input("enter no of virtices"))
edge=int(input("enter no of edge"))
arr=[[0 for _ in range(vir)]for _ in range(vir)]
print(len(arr[0]))
print(len(arr))
for i in range(edge):
    node1=int(input("enter node1 "))
    node2=int(input("enter node2 "))
    weight=int(input("enter weight"))
    graphs(arr,node1,node2,weight)



disp(arr)




