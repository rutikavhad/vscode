class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height=0


class BST:
    def __init__(self):
        self.root = None

    # Insert a value
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

 
    # Search for a value
    def search(self, value):
        return self._search(self.root, value)

    def _search(self, current, value):
        if current is None:
            return False
        if current.value == value:
            return True
        elif value < current.value:
            return self._search(current.left, value)
        else:
            return self._search(current.right, value)

    # Inorder Traversal (sorted output)
    def inorder(self):
        self._inorder(self.root)
        print()

    def _inorder(self, current):
        if current:
            self._inorder(current.left)
            print(current.value, end=" ")
            self._inorder(current.right)


tree = BST()

tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)
tree.insert(60)
tree.insert(80)

print("Inorder traversal:")
tree.inorder()   # Output: 20 30 40 50 60 70 80

print("Search 40:", tree.search(40))  # True
print("Search 100:", tree.search(100))  # False