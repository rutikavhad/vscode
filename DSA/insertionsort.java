public class insertionsort {


    public static int insertionsortt(int[] arr){
        for (int i = 0; i < arr.length-1; i++) {
            for (int j = i+1; j >0; j--) {
                if (arr[j]<arr[j-1]) {
                    int temp=arr[j];
                    arr[j]=arr[j-1];
                    arr[j-1]=temp;
                }
                else
                break;   
            }
        }
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
        return 0;
    }
    public static void main(String[] args) {
        
        int arr[]={9,8,7,-6,7,5,4,3,2,12-22};
        insertionsortt(arr);

        
    }    
}
