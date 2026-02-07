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
        while curr.next: #if not None then run it
            curr=curr.next
        curr.next=newnode

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
   


list=Linked()

list.add(12)
list.add(13)
list.add(14)
list.add(15)
list.add(16)
list.add(17)

list.display()