class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1   # NEW


class AVL:
    def __init__(self):
        self.root = None


    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)


    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        # rotation
        y.right = z
        z.left = T3

        # update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        # rotation
        y.left = z
        z.right = T2

        # update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # Insert
    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        # 1. Normal BST insert
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        # 2. Update height
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

        # 3. Get balance
        balance = self.get_balance(node)

        # 4. Handle 4 cases

        # LL
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)

        # RR
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)

        # LR
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RL
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    #Inorder 
    def inorder(self):
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            print(node.value, end=" ")
            self._inorder(node.right)