class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        index = self.hash_function(key)
        i = 1

        while self.table[index] is not None:
            index = (self.hash_function(key) + i*i) % self.size
            i += 1

        self.table[index] = key

    def display(self):
        print(self.table)


ht = HashTable(10)

ht.insert(15)
ht.insert(25)
ht.insert(35)

ht.display()