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
    def remove(self,tar):
        cur=0
        target=tar+1
        size=self.size()
        size+=1
        # print(size)
        if self.root is None:
            return 0
        else:
            temp=self.root
            while self.root is not None:
                cur+=1
                if size-cur==(size-1) and target==(size):
                    self.root=self.root.next
                    return
                elif size-cur==target:
                    B=self.root.next
                    self.root.next=B.next
                    # return
                else:
                    self.root=self.root.next
            self.root=temp
                
    # def reremove(self,target):
    #     dummy = link()
    #     dummy.next = self.root

    #     fast = dummy
    #     slow = dummy

    #     for _ in range(target + 1):
    #         fast = fast.next

    #     while fast:
    #         fast = fast.next
    #         slow = slow.next

    #     slow.next = slow.next.next

    #     return dummy.next







# class nano:
#     def runit(s,numRows):





s=link()
s.insert(1)
s.insert(2)
s.insert(3)
s.insert(4)
s.insert(5)
s.insert(6)
s.insert(7)

s.disp()
s.remove(7)
print("")
s.disp()
# print("")
# s.reremove(7)
# s.disp()

# print(len(n))

