
class Node{

    int data;
    Node next;

    //constructer
    Node(int value){
        data=value;
        next=null;
    }
}
public class linkedlist {
  Node head;
  
  void insert(int num){
    Node newnNode=new Node(num);
    
    if(head==null){
        head=newnNode;
        return;
    }
    Node temp =head;
    while (temp.next!=null) {
        temp=temp.next;
    }
    temp.next =newnNode;
    
}

  void display(){
    Node temp=head;
    //System.out.println(head);
    while (temp!=null) {
        System.out.print(" => "+temp.data);
        //System.out.println(" => ");
        temp=temp.next;
    }
    System.out.println("NULL");
  }

  //delete head

  void delete(){
    if (head!=null) {
      System.out.println("deleted "+head.data);
      head=head.next;
     
    }
    else
    System.out.println("head is null");
  }


  public static void main(String[] args) {
  linkedlist link =new linkedlist();
  link.insert(11);
  link.insert(12);
  link.insert(13);
  link.insert(14);
  link.insert(15);
  link.display();
  link.delete();
  link.display();
  }
}
