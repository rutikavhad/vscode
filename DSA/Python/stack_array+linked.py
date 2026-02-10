class Node:
    def __init__(self,data):
        self.next=None
        self.prev=None
        self.data=data

    



class Linked:
    def __init__(self):
        self.head=None
    
    def add(self,num):
        newnode=Node(num)
        if self.head is None:
            self.head=newnode
            return
        curr=self.head
        while curr.next is not None: #if not None then run it
            curr=curr.next
        curr.next=newnode

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


    def push(self,data): #last in first out 
        temp=self.head
        newnode=Node(data)
        while temp.next is not None:
            temp=temp.next
        temp.next=newnode
    

    def pop(self): #first out
        temp=self.head
        while temp.next.next is not None:
            temp=temp.next
        temp.next=None

        



   

#by array linked list

# FOR UNKNOWN SIZE USE .APPEND() # ALL TIME USE IT THIS GOOD  THIS ALSO WORKK  arr=[None]*n

nn=5
n=int(nn)
arr=[0]*n

def disp():
    for i in range(len(arr)):
        print(arr[i])
def add():
    for i in range(n):
        arr[i]=i
        #print(arr[i])
    

def pop():   #first in last out
    size=len(arr)-1
    while arr[size] is None:
        size-=1
    arr[size]=None


def push(num):
    arrr=[0]*1
    arrr[0]=num
    arr.extend(arrr)

    for i in range(len(arr)-1,0,-1):
        temp=arr[i]
        arr[i]=arr[i-1]
        arr[i-1]=temp


# add()

# push(12)
# push(13)
# pop()
# pop()
# push(14)
# push(15)
# pop()
# pop()
# push(16)
# push(17)
# pop()
# pop()
# disp()

 

