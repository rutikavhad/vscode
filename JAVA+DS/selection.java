public class selection{
     public static int getmax(int[] arr,int a,int last){
        int max=0;
        for (int i = 0; i <= last; i++) {
            
            if (arr[max]<arr[i]) {
                max=i;
            }
            
        }
       // System.err.println("from function"+max);
        return max;
    }
    public static void main(String[] args) {
        int arr[]={};
        //int last=1;
        for (int i = 0; i < arr.length; i++) {
            int last=arr.length-1-i;
            int max=getmax(arr,0,last);
            //System.err.println(max);
                int temp=arr[max];
                arr[max]=arr[last];
                arr[last]=temp;
            
        }

        for (int i = 0; i < arr.length; i++) {
            System.err.println(arr[i]);
        }
    }
}