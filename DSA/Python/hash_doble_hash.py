class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def h1(self, key):
        return key % self.size

    def h2(self, key):
        return 7 - (key % 7)

    def insert(self, key):
        index = self.h1(key)

        i = 0
        while self.table[index] is not None:
            index = (self.h1(key) + i * self.h2(key)) % self.size
            i += 1

        self.table[index] = key

    def display(self):
        print(self.table)


ht = HashTable(10)

ht.insert(10)
ht.insert(20)
ht.insert(30)

ht.display()