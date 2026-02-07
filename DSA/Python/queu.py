class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_number(self, number):
        new_node = Node(number)

        # If list is empty
        if self.head is None:
            self.head = new_node
            return
        # Traverse to the end
        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


    def dequeuF(self):
        print(f"head remove {self.head.data}")
        self.head=self.head.next
        
        

    def dequeuR(self):
        temp=self.head
        while temp:
            if temp.next.next is None:
                print(f"rear remove {temp.next.data}")
                temp.next=None
                return
            else:
                temp=temp.next
        
    def enqueuF(self,data):
        temp=self.head
        newnode=Node(data)        
        self.head=newnode
        self.head.next=temp
        print(f"added at Front {self.head.data}")
        return


    
    def enqueuR(self,dat):
        newnode=Node(dat)
        temp=self.head
        while temp:
            if temp.next is None:
                temp.next=newnode
                print(f"added at rear {temp.next.data}")
                temp.next.next=None
                return
            else:
                temp=temp.next



    def circuler(self):
        temp=self.head
        while(8):
            if temp.next is not None:
                 print(temp.data)
                 temp=temp.next
            else:
                if temp.next is None:
                    temp.next=self.head
                    print(f"next is after last {temp.next}")
           





            

list=LinkedList()
list.add_number(12)
list.add_number(13)
list.add_number(15)
list.add_number(16)
list.add_number(17)
list.add_number(18)
list.display()
list.dequeuF()
list.dequeuR()
list.enqueuF(19)
list.enqueuR(20)
list.display()

list.circuler()


