class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:

    def __init__(self, size):
        self.size = size
        self.table = [None] * size


    def hash_function(self, key):
        return key % self.size


    def insert(self, key, value):

        index = self.hash_function(key)

        new_node = Node(key, value)

        if self.table[index] is None:
            self.table[index] = new_node

        else:
            current = self.table[index]

            while current.next:
                current = current.next

            current.next = new_node


    def search(self, key):

        index = self.hash_function(key)

        current = self.table[index]

        while current:

            if current.key == key:
                return current.value

            current = current.next

        return None


    def display(self):

        for i in range(self.size):

            print(i, end=" → ")

            current = self.table[i]

            while current:
                print(f"({current.key},{current.value})", end=" → ")
                current = current.next

            print("None")


ht = HashTable(5)

ht.insert(12, "A")
ht.insert(22, "B")
ht.insert(32, "C")

ht.display()

print("Search 22:", ht.search(22))