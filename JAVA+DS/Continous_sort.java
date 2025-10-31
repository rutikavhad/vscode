public class Continous_sort {
    public static int themissing(int a[]){
        int min=a[0];
        for (int j = 0; j < a.length; j++) {
            if(min>a[j]){
                min=a[j];
            }  
        }
       // System.out.println("min is "+min);
        int pos;
        for (int i = 0; i < a.length; i++) {
            pos=a[i]-min;
            int temp=a[pos];
            a[pos]=a[i];
            a[i]=temp;
        }
        for (int i = 0; i < a.length; i++) {
            System.err.println(a[i]);
        }
        return 0;
    }
    public static void main(String[] args) {
        int a[]={2,1,0};
        themissing(a);
        
    }
}