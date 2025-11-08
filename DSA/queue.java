class Node {
    int data;
    Node next;
    Node prev;
    Node(int value){
        data=value;
        next=null;
        prev=null;
    }
}
public class queue {
    Node front;
    Node rear;
    //push first
    void push(int num){
        Node newnode=new Node(num);
        if (rear==null) {
           front = rear = newnode;
         // System.out.println("push"+front.data);
          

        }else{
            rear.next=newnode;
            newnode.prev=rear;
            rear=newnode; 
          // System.out.println("push"+front.data);
    } 
    System.out.println("push"+num);    
    }
    //pop first 
    void pop(){
        if (front==null) {
            System.out.println("queue is empty");
	   return;
        }
        System.out.println("pop"+front.data);
	    front=front.next;
	    if(front!=null)
		front.prev=null;
        else
        rear=null;
    }
    void seek(){
        
        if (front==null) {
            System.out.println("queue is empty"); 
        }
        else
        System.out.println("top ele is  "+front.data);
    }
    void display(){
        Node temp=front;
        while (temp!=null) {
            System.out.println("display is "+temp.data);
            temp=temp.next;
        }
    }
    public static void main(String[] args) {
        queue queue=new queue();
        queue.push(12);
        queue.push(44);
        queue.push(43);
        queue.pop();//12
        //queue.seek();
        queue.pop();//44
        queue.pop();//43
        queue.pop();//empty
        queue.seek();//empty if not any ele
        queue.push(55);
        queue.seek();
        queue.display();
    } 
}
