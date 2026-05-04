# class Node:
#     def __init__(self,value,capa=10):
#         self.values=value
#         self.next=None
    


    

# class link:
#     def __init__(self):
#         self.root=None
#     def insert(self,value):
#         if self.root is None:
#             self.root=Node(value)
#             return
#         temp=self.root
#         while temp.next is not None:
#             temp=temp.next
#         temp.next=Node(value)
#     def disp(self):
#         if self.root is None:
#             return 0
#         temp=self.root
#         while temp is not None:
#             print(temp.values)
#             temp=temp.next
#     def fmid(self):
#         if self.root is None:
#             return
#         temp1=self.root
#         temp2=self.root
#         # print(temp2.values)
#         while temp2 is not None and temp2.next is not None:
#             temp1=temp1.next
#             temp2=temp2.next.next
#         print(temp1.values)





s=["king","king"]

print(id(s[0]))
print(id(s[1]))