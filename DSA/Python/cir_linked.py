class Node:
    def __init__(self,data):
        self.next=None
        self.data=data

class cirlink:
    def __init__(self):
        self.root=None
    

    def insert(self,data):
        temp=self.root
        if self.root is None:
            self.root=Node(data)
            self.root.next=self.root
        else:
            while temp.next is not self.root:
                temp=temp.next
            newnode=Node(data)
            temp.next=newnode
            newnode.next=self.root



    def display(self):
        temp=self.root
        if self.root is None:
            return
        else:
            
            while True:
                if temp.next.next!=self.root.next:
                    print(temp.data)
                    temp=temp.next
                else:
                    return


    def find(self):
        temp=self.root
        while True:
            if temp.next==self.root:
                return True
            elif temp.next==None:
                return False
            else:
                temp=temp.next

cir=cirlink()
cir.insert(12)
cir.insert(13)
cir.insert(14)
cir.insert(15)
cir.insert(16)

cir.display()
print(cir.find())
