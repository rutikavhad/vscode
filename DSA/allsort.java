

class allsort {

//this bubble sort
public static int bubble(int[] arr){

        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < i; j++) {    
                if(arr[i]<arr[j]){
                    int temp=arr[i];
                    arr[i]=arr[j];
                    arr[j]=temp;
                }
            }
        }

    return printt(arr);
}

//this selection sort
    public static int getmax(int[] arr,int a,int last){
        int max=arr[0];
        for(int i=0;i<last;i++){
            if(arr[max]<arr[i]){
                //System.out.println("hello");
                max=i;
            }
        }
        return max;
    }
    public static int selection(int[] arr){
        for(int i=0;i<arr.length;i++){
            int last=arr.length-1-i;
            int max=getmax(arr,0, last);

            int temp=arr[max];
            arr[max]=arr[last];
            arr[last]=temp;
        }
        return printt(arr);
    }


//this insertion sort
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
        return printt(arr);
    }
    //print function
public static int printt(int[] arr){
    for (int i = 0; i < arr.length-1; i++) {
        System.out.println(arr[i]);
    }
    return 0;
}
    public static void main(String[] args) {
        int[] arr={4,3,5,6,4,3,4,5,5,22,1,1};

        //bubble(arr);//work

        //selection(arr); //work

        insertionsortt(arr);
    }
}