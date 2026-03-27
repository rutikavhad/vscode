class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, value):
    if root is None:
        return Node(value)

    if value < root.data:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)

    return root




root = None
for i in [10, 20, 30, 40, 50, 25]:
    root = insert(root, i)


def display(root):
    if root is None:
        return

    print(root.data, end="  ")
    display(root.left)
    display(root.right)

def inorder(root):
    if root:
        inorder(root.left)
        print(root.data,end="  ")
        inorder(root.right)

def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.data,end="  ")



def find(root,key):
    if root:
        find(root.left,key)
        find(root.right,key)
        if root.data == key:
            return print(key)



print("Preorder ",display(root))
print()
print("inorder ",inorder(root))
print()
print("postorder ",postorder(root))

find(root,40)
