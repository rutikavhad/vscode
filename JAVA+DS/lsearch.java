public class lsearch{
    public static void main(String[] args) {
            int [] num={12,94,23,34,54,65,36,38,23};
            int tarter=34;

       int ans= lenearsearch(num,tarter);
       System.out.println(ans);
        
    }

    static int lenearsearch(int arr[],int target){

        if(arr.length==0){
            return -1;
        }
        for (int i = 0; i < arr.length; i++) {
            //ceck for element is reual to targer
            int ele=arr[i];
            if(ele==target){
                return i; 
            }
        }
        return -1;

    }

}