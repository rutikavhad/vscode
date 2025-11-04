class Node{
    static int value;
    Node next;
    Node prev;
    Node(int data){
        data=value;
        next=null;
        prev=null;
    }
}
public class hashing_linear {
   Node hade;                           //linkedlist
   int arr[]=new int[10];               //this is array data
    void test(){
        arr[3]=12;
        Node.value=arr[3];
        System.out.println(Node.value);
      
    }
    void newhash(int number){
        
    }
    public static void main(String[] args) {
        hashing_linear hash=new hashing_linear();
        hash.test();

    }
    
}
