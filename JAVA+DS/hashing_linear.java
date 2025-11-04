class Node{
    int data;
    Node next;
    Node prev;
    Node(int value){
        value=data;
        next=null;
        prev=null;
    }
}
public class hashing_linear {
   Node head;                           //linkedlist
   int arr[]=new int[10];               //this is array data
    void newhash(int number){
        Node newnNode=new Node(number);
        int key=number%arr.length;
        if (arr[key]==0){
            arr[key]=number;
            head=newnNode;
            System.out.println("by link"+head.data);
            System.out.println("by array"+arr[key]);
        }
        
    }
    public static void main(String[] args) {
        hashing_linear hash=new hashing_linear();
       // hash.test();
        hash.newhash(12);

    }
    
}
