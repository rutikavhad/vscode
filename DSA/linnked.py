class Node:
    def __init__(self,data):
        self.data=data
        self.next=None


Node1=Node(11)

Node2=Node(12)

Node3=Node(13)

Node4=Node(14)

Node1.next=Node2
Node2.next=Node3
Node3.next=Node4

cur=Node1
while cur:
    print(cur.data)
    cur=cur.next


