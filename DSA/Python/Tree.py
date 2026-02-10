class Node:
    def __init__(self,data):
        self.parent=None
        self.child=[]
        self.data=data

#USED IN FILE SYSTEM

class Tree:
    def __init__(self):
        self.head=None

    def add(self,num):
        print("root")
        #root>left_child,right_child
        self.head=Node(10)
        root=self.head
        
        print(root)
        child1=Node(11)
        child2=Node(12)
        root.child.append(child1)
        root.child.append(child2)
        print(root.child[0].data)#11
        print(root.child[1].data)#12
        print("child memory addr")
        print("left ",root.child[0])
        print("right ",root.child[1])
        parr=Node(root.child[0])
        parr.parent=root
        print("parent of left child is ",parr.parent.data)

        # add child to parent of child node 
        # LEFT SIDE
        #root>left_child(parent)>left_child,right_child
        print("left of root")

        print(root.child[0]) # this print address of child 0 
        temp=root
        temp=Node(temp.child[0]) # this do a child as next root   
       
        child3=Node(13)
        child4=Node(14)
        temp.child.append(child3)
        temp.child.append(child4)
        print(temp.child[0].data)
        print(temp.child[1].data)
        
        # RIGHT SIDE
        print("right of root")

        #root>right_child(parent)>left_child,right_child
        print(root.child[1]) # this print address of child 0 
        temp=root
        temp=Node(temp.child[1]) # this do a child as next root   
       
        child3=Node(15)
        child4=Node(16)
        temp.child.append(child3)
        temp.child.append(child4)
        print(temp.child[0].data)
        print(temp.child[1].data)
 

    def chil(self,num):
        temp=self.head
        if temp.data==num:
            print(f"parent {temp.data} left child= {temp.child[0].data} and right child is = {temp.child[1].data}")
        else:
            while temp.data != num:
                temp=temp.child[0]
                
            print(temp.data)












tree=Tree()
tree.add(32)
tree.chil(11)