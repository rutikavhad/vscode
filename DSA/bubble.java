public class bubble {
    public static void main(String[] args) {
        int arr[]={3,1,5,4,2,5,9,5,56,7,5,6};
        for(int i=0;i<arr.length;i++){
            for (int j = 0;j<i ; j++){
                if(arr[i]<arr[j]){
                    int temp=arr[i];
                    arr[i]=arr[j];
                    arr[j]=temp;
                }

            }
                
            }
            for (int i = 0; i < arr.length; i++) {
                System.err.println(arr[i]);
            }
        }

    }
