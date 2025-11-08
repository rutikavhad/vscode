public class twodarraaryserch{
    public static void main(String[] args) {
        int[][] arr ={
            {12,12,12,23,34,},
            {3,4,5,6,7},
            {8,6,4,2,4},
            {9,0,7,56,8}
        };
        int target=34;
        int taregt=0;
        System.out.println(search(arr,target));
        System.out.println(max(arr,taregt) );

    }
    static int search(int[][] arr , int target){

        for(int i=0;i<arr.length;i++){
            for(int j=0;j<arr[i].length;j++){
                if(target==arr[i][j]){
                    return target;
                }
            }
        }
        return 0;
    }
    static int max(int[][] arr,int taregt){
        taregt=arr[0][0];
      for(int i=0;i<arr.length;i++){
            for(int j=0;j<arr[i].length;j++){
                if(taregt<arr[i][j]){
                    taregt=arr[i][j];
                }
            }
        }
        return taregt;
    }
}

