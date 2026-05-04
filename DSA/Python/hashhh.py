class node:
    def __init__(self,key,data):
        self.data=data
        self.key=key
        self.next=None


class hashmap:
    def __init__(self,capacity=10):
        self.capacity=capacity
        self.buckets=[None]*capacity


    def _hash(self,key):
        return key%self.capacity
    

    def put(self,key,data):
        index=self._hash(key)
        head=self.buckets[index]

        curr=head
        while curr:
            if curr.key==key:
                curr.data=data
                return
            curr=curr.next
        new_node=node(key,data)
        new_node.next=head
        self.buckets[index]=new_node



    def get(self,key):
        index=self._hash(key)
        curr=self.buckets[index]

        while curr:
            if curr.key==key:
                return curr.data
            curr=curr.next
        return -1
    



hm=hashmap()
hm.put(1,10)
hm.put(11,20)

print(hm.get(1))
print(hm.get(11))
