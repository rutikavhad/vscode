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
  // Node head;                           //linkedlist
   Node arr[]=new Node[10];               //this is array data
    void newhash(int number){
        Node newnode=new Node(number);
        int key=number%arr.length;
        if (arr[key]==null){
            arr[key]=newnode;
            //System.out.println("by link"+head.data);
        }
        else{
            Node temp=arr[key];
            while (temp.next!=null) {
                temp=temp.next;                
            }
            temp.next=newnode;
        } 
}
    void display() {
        for (int i = 0; i < arr.length; i++) {
            System.out.print("Bucket " + i + ": ");
            Node temp = arr[i];
            while (temp != null) {
                System.out.print(temp.data + " -> ");
                temp = temp.next;
            }
            System.out.println("null");
        }
    }

    public static void main(String[] args) {
        hashing_linear hash=new hashing_linear();
       // hash.test();
        hash.newhash(12);
        
        hash.display();

    }
    
}
