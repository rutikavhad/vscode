class Node {
    int data;
    Node next;
    Node prev;
    Node(int value){
        data=value;
        next=null;
    }
}
public class stack {
    Node head;
    //push first
    void push(int num){
        Node top=new Node(num);
        if (head==null) {
            head=top;
            System.out.println("push"+head.data);
        }else{
            top.prev=head;
            head.next=top;
            head=top; 
             System.out.println("push"+head.data);
    }     
    }
    //pop first 
    void pop(){
        if (head!=null) {
            System.out.println("pop"+head.data);
            head=head.prev;
            if (head.next!=null) {
                head.next=null;
            }
        }
        else
        System.out.println("stack is empty");
    }
    void seek(){
        if (head==null) {
            System.out.println("stack is empty"); 
        }
        else
        System.out.println("top ele is  "+head.data);
    }
    void display(){
        Node temp=head;
        while (temp!=null) {
            System.out.println("display is "+temp.data);
            temp=temp.prev;
        }
    }
    public static void main(String[] args) {
        stack stack=new stack();
        stack.push(12);
        stack.push(44);
        stack.push(43);
        stack.pop();
        stack.seek();
        stack.pop();
        stack.seek();
        stack.display();
    } 
}
