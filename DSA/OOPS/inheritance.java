// public class inheritance{
//     int sum(int a,int b,int c){
//         int k;
//         k=a+b+c;
//         System.out.println(k);
//         return 0;

//     }
//     int sum(int a,int b){
//         System.out.println(a+b);
//         return 0;
//     }

//     public static void main(String[] args){
//         inheritance pk=new inheritance();
//         pk.sum(1,2,3);
//         pk.sum(1,2);

//     }
// }


public class inheritance extends parent{
    int sum(int a,int b){
        return a-b;
    }

    public static void main(String[] args){
        inheritance obj=new inheritance();

        obj.sum(1,2);
    }

}