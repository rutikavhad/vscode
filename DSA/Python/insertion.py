# arr=[4,5,3,1,2]

# #for i in range(0,10,2) for(i=0;i<10;i+=2) op:-  0, 2, 4, 6, 8

# # for i in range(20,10,-2) for(i=20;i>10;i-=2):-20, 18, 16, 14, 12


# for i  in range (len(arr)-1):
#     for j in range(i+1,0,-1):  #for(j=i+1,j>0;j--)
#         if arr[j]<arr[j-1]:
#             temp=arr[j]
#             arr[j]=arr[j-1]
#             arr[j-1]=temp
#         else:
#             break

# print(arr)

# for i in range(10):
#     for j in range(i+1,0,-1):
#         print(j)


class Node:
    def __init__(self,data):
        self.data=data
        self.next=None


class linked:
    def __init__(self):
        self.root=None

    def insert(self,value):
        if self.root is None:
            self.root=Node(value)
        else:
            temp=self.root
            while temp.next is not None:
                temp=temp.next
            temp.next = Node(value)





    def display(self):
        temp=self.root
        if temp is None:
            return
        else:
            while temp is not None:
                print(temp.data)
                temp=temp.next

    def delete(self,value):
        temp=self.root
        if self.root is None:
            return
        else:
            if self.root.data==value:
                self.root=self.root.next
                return
            else:
                while self.root.next is not None:
                    if self.root.next.data==value:
                       # print(f"{temp.data} > {temp.next.data} > {temp.next.next.data}")
                        self.root.next=self.root.next.next
                        # print(f"{temp.data} > {temp.next.data} > {temp.next.next.data}")

                    else:
                        self.root=self.root.next
        self.root=temp
        print(self.root.data)
    

    def find(self):
        temp=self.root
        while True:
            if temp.next==self.root:
                return True
            elif temp.next==None:
                return False
            else:
                temp=temp.next







node=linked()
node.insert(12)
node.insert(13)
node.insert(14)
node.insert(15)
node.insert(16)

node.display()

node.delete(13)
node.display()
print(node.find())

