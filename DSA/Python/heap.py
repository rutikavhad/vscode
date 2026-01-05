# data=["A","B","C","D","E","F","G"]
    # 0,1,2,3,4,5,6,7,8
#node at index= i
# i left child at 2*i
# i right child at 2*i+1
#  i parent at i/2


# left=i*2
# right=2*i+1
# parent=i/2
# print("left child of ",data[0],"is ",data[left],"\n")
# print("left child of ",data[0],"is ",data[left],"\n")
# print("left child of ",data[0],"is ",data[left],"\n")

#full binay tree all hight of tree are same 
# complete binary from frit and last element no any missing element
#not complete binary tree is from 1st last missing one or more element
#for complete binary requrid full left to right elements

# MIN/MAX HEAP

#MAX=
#          50
#    30              20
#20      16      12      8

#MIN=
#            8
#     10             12
# 16     20     30       40


#INSERT IN MAX HEAP


max_heap=[50,30,20,16,12,10,8]

class Node:
    def __init__(self,value):
        self.value=value
        self.next=None

# node=Node(50)
# node.next=Node(30)
# node.next.next=Node(20)
# node.next.next.next=Node(16)
# head=node # this for without loss old data use temp head to print
# for i in range(4):  #node is not None this not be work
#     print(node.value) # normal 4 values will work
#     node=node.next

# while head is not None: # this are best
#     print(head.value)
#     head=head.next

head=node
n=int(input("enter how many linked  list you want "))

for i in range(0,n):
    new_node=int(input(f"enter{i}st number"))
    if head==None:
        head=new_node
    else:
        current=head
        while current.next is not Node:
            current=current.next

        current.next=new_node


print(f"added{new_node}")
