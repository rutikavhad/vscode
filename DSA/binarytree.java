class Node{
    int data;
    Node left,right;
    Node(int data){
        this.data=data;

    }
}
public class binarytree {
    Node head;
    void inorder(Node number){
        if (number == null) return;
        inorder(number.left);
        System.out.print(number.data + " ");
        inorder(number.right);

    }
    void preorder(Node number){
        if(number==null)return;
        System.out.print(number.data+" ");
        preorder(number.left);
        preorder(number.right);

    }
    void postorder(Node number){
        if(number==null)return;
        postorder(number.left);
        postorder(number.right);
        System.out.print(number.data+" ");
    }


    public static void main(String[] args) {
        binarytree tree=new binarytree();
        tree.head=new Node(1);
        tree.head.left=new Node(2);
        tree.head.left.left=new Node(3);
        tree.head.left.right=new Node(4);
        tree.head.right=new Node(5);
        tree.head.right.left=new Node(6);
        tree.head.right.right=new Node(7);

        System.out.print("Inorder =");
        tree.inorder(tree.head);
        System.out.print("\nPreorder =");
        tree.preorder(tree.head);
        System.out.print("\nPostorder =");
        tree.postorder(tree.head);



    }
    
}
