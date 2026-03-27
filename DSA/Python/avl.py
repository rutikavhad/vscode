class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.h = 1

def height(n):
    return n.h if n else 0

def balance(n):
    return height(n.left) - height(n.right) if n else 0

def right_rotate(y):
    x = y.left
    y.left = x.right
    x.right = y
    y.h = 1 + max(height(y.left), height(y.right))
    x.h = 1 + max(height(x.left), height(x.right))
    return x

def left_rotate(x):
    y = x.right
    x.right = y.left
    y.left = x
    x.h = 1 + max(height(x.left), height(x.right))
    y.h = 1 + max(height(y.left), height(y.right))
    return y

def insert(root, key):
    if not root:
        return Node(key)

    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
#used to balance tree
    root.h = 1 + max(height(root.left), height(root.right))
    b = balance(root)

    if b > 1 and key < root.left.val:
        return right_rotate(root)
    if b < -1 and key > root.right.val:
        return left_rotate(root)
    if b > 1 and key > root.left.val:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if b < -1 and key < root.right.val:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# Preorder Traversal
def preorder(root):
    if root:
        print(root.val, end=" ")
        preorder(root.left)
        preorder(root.right)

# Inorder Traversal
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val, end=" ")
        inorder(root.right)

# Postorder Traversal
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val, end=" ")


# Example
root = None
for i in [10, 20, 30, 40, 50, 25]:
    root = insert(root, i)

print("pre")
preorder(root)
print()
print("in")
inorder(root)
print()
print("post")
postorder(root)