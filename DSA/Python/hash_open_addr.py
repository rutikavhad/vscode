class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)

        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def display(self):
        for i in range(self.size):
            print(i, ":", self.table[i])


ht = HashTable(10)

ht.insert(15, "A")
ht.insert(25, "B")
ht.insert(35, "C")

ht.display()