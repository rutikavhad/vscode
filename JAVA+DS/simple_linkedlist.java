class Node{
    int data;
    Node next; //forword
    Node prev; //backword
}
public class simple_linkedlist {
    public static void main(String[] args) {
        Node a1=new Node();
        Node a2=new Node();
        Node a3=new Node();
        Node a4=new Node();
        Node a5=new Node();
        Node a6=new Node();
        Node a7=new Node();
        Node a8=new Node();
        //allocate data into node
        a1.data=12;
        a2.data=32;
        a3.data=5;
        a4.data=21;



        //link each node to others connected with forword
        a1.next=a2;
        a2.next=a3;
        a3.next=a4;
        a4.next=null;
        //try delete a2
        a1.next=a3;// a2 32 deleted 
        //try to ADD NEW IN  a2
        a2.data=43;
        a1.next=a2;
        a2.next=a3;
        //display list by forword
        Node cur=a1;
        System.out.println("forword link");
        while (cur!=null) {
            System.out.print("=>"+cur.data);
            cur=cur.next;
        }

        // for backword display
        a5.data=15;
        a6.data=14;
        a7.data=13;
        a8.data=12;


        //link backword
        // a5 to a8
        a8.next=null;
        a8.prev=a7;
        a7.prev=a6;
        a6.prev=a5;
        a5.prev=null;


        //add new ele
        Node a9=new Node();
        a9.data=11;

        a9.next=null;
        a9.prev=a8;



        //dispaly backword 
        Node curr=a9;
        System.out.println("\nbackword link");
        while (curr!=null) {
            System.out.print("=>"+curr.data);
            curr=curr.prev;
        }

        
    }

   
    
}