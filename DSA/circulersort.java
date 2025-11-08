public class circulersort {

    public static int circulersortt(int[] arr){
        //first find minimum
        int min=arr[0];
        for (int i = 0; i < arr.length; i++) {
            if (min>arr[i]) {
                min=arr[i];
            }
        }
        int start=0;
        for (int i = 0; i < arr.length; i++) {
            start=arr[i]-min;
            
        }
        return 0;
    }
    public static void main(String[] args) {
        int arr[]={12,11,13,10,9,8,7};
        circulersortt(arr);
    }    
}
