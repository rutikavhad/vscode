class Node:
    def __init__(self,value):
        self.value=value
        self.next=None
    
class link:
    def __init__(self):
        self.root=None
    
    def insert(self,value):
        if self.root is None:
            self.root=Node(value)
        else:
            temp=self.root
            while temp.next is not None:
                temp=temp.next
            temp.next=Node(value)
            
        
    
    def disp(self):
        if self.root is None:
            print("hello")
            return None
        else:
            temp=self.root
            while temp is not None:
                print(temp.value,end=" => ")
                temp=temp.next
            if temp is None:
                print(None)
    def size(self):
        count=0
        if self.root is None:
            return count
        else:
            temp=self.root
            while temp is not None:
                count+=1
                temp=temp.next
        return count
    def remid(self):
        cur=0
        size=self.size()
        # size=7
        print(size/2)
        temp=self.root
        if (size/2)-int(size/2)==0.5:
            # print(int((size/2)+1))
            # print("yes")
            while self.root is not None:
                cur+=1
                if int(size/2)==cur:
                    B=self.root.next
                    self.root.next=B.next
                else:
                    self.root=self.root.next
            self.root=temp
        else:
            while self.root is not None:
                cur+=1
                if int(size/2)==cur:
                    B=self.root.next
                    self.root.next=B.next
                else:
                    self.root=self.root.next
            self.root=temp


s=link()
# s.insert(23)
# s.disp()
for i in range(5,11):
    s.insert(i)
s.disp()
s.remid()
print("")
s.disp()

