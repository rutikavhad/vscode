class Node {
    int data;
    Node left, right;
    Node(int data) { this.data = data; }
}

class BST {
    Node root;

    Node insert(Node root, int key) {
        if (root == null) return new Node(key);
        if (key < root.data) root.left = insert(root.left, key);
        else if (key > root.data) root.right = insert(root.right, key);
        return root;
    }

    void inorder(Node root) {
        if (root == null) return;
        inorder(root.left);
        System.out.print(root.data + " ");
        inorder(root.right);
    }

    boolean search(Node root, int key) {
        if (root == null) return false;
        if (root.data == key) return true;
        return key < root.data ? search(root.left, key) : search(root.right, key);
    }

    Node delete(Node root, int key) {
        if (root == null) return null;

        if (key < root.data)
            root.left = delete(root.left, key);
        else if (key > root.data)
            root.right = delete(root.right, key);
        else {
            if (root.left == null) return root.right;
            else if (root.right == null) return root.left;
            root.data = minValue(root.right);
            root.right = delete(root.right, root.data);
        }
        return root;
    }

    int minValue(Node node) {
        int min = node.data;
        while (node.left != null) {
            min = node.left.data;
            node = node.left;
        }
        return min;
    }
}

public class BSTS {
    public static void main(String[] args) {
        BST tree = new BST();
        Node root = null;

        int[] arr = {8, 3, 10, 1, 6, 14, 4, 7, 13};
        for (int val : arr)
            root = tree.insert(root, val);

        System.out.print("Inorder Traversal: ");
        tree.inorder(root);

        System.out.println("\nSearch 7: " + tree.search(root, 7));
        System.out.println("Search 2: " + tree.search(root, 2));

        System.out.println("\nDelete 10:");
        root = tree.delete(root, 10);
        tree.inorder(root);
    }
}
