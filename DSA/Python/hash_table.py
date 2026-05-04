class Node:
    def __init__(self,value,key):
        self.value=value
        self.key=key
        self.next=None


class dj:
    def __init__(self):
        self.array=[None]*10

    
    def intadd(self,key,value):
        h=key%10
        # print(h)
        if self.array[h] is None:
            self.array[h]=Node(value,key)
            return
        temp=self.array[h]
        while temp.next is not None:
            temp=temp.next
        temp.next=Node(value,key)


    def find(self,key):
        h=key%10
        if self.array[h] is None:
            print("None")
            return "None"
        if self.array[h].key is key:
            print(self.array[h].value)
            return
        temp=self.array[h]
        while temp.key is not key and temp.next is not None:
            temp=temp.next
        if temp.key is key:
            print(temp.value)
        else:
            print("not Find")

        
    def delete(self, key):
        h = key % len(self.array)

        if self.array[h] is None:
            return

        if self.array[h].key == key:
            self.array[h] = self.array[h].next
            return

        temp = self.array[h]

        while temp.next is not None and temp.next.key != key:
            temp = temp.next

        if temp.next is not None:
            temp.next = temp.next.next
        else:
            print("not found")


# def delete(self,key):
#     h=key%10 
#     if self.array[h] is None:
#         return 
#     if self.array[h].key == key: 
#         self.array[h]=self.array[h].next 
#         return 
#     temp=self.array[h]
#     while temp.next is not None and temp.next.key != key : 
#         temp=temp.next 
#     if temp.next is not None: 
#         temp.next=temp.next.next
#     else: print("not Find")
    
    

dj=dj()
dj.intadd(12,"king")
dj.intadd(13,"raja")
dj.intadd(14,"rutik")
dj.intadd(15,"don")
dj.intadd(16,"jhon")
dj.intadd(17,"kong")
dj.intadd(27,"kong1")
dj.intadd(47,"kong2")
dj.intadd(37,"kong3")

# dj.find(87)
dj.delete(55)
dj.find(37)


class Node:
    def __init__(self,value,key):
        self.value=value
        self.key=key
        self.next=None


class listd:
    def __init__(self):
        table=[None]*10
    
class Node:
    def __int__(self,value):
        self.value=value
        self.next=None
        self.prev=None

class lost:
    def __init__(self):
        self.root=None
        