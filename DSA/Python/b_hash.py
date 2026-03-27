class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index] = value

    def search(self, key):
        index = self.hash_function(key)
        return self.table[index]

    def display(self):
        for i in range(self.size):
            print(i, ":", self.table[i])


ht = HashTable(10)

ht.insert(21, "A")
ht.insert(13, "B")
ht.insert(15, "C")

ht.display()

print("Search key 13:", ht.search(13))