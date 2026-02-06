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


    def dequeu(self):
        print(self.head.data)
        self.head=self.head.next
        print(f"new {self.head.data}")
    def enqueu(self,data):
        while data:
            

list=LinkedList()
list.add_number(12)
list.add_number(13)
list.dequeu()


