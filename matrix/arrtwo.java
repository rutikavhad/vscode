

public class arrtwo{
    public static void main(String[] args) {
        int arr[]={1,2,3,1,2,4,5,6,5,6,9,6,5};

        int target=11;
        int old;
        int ne=0;

        for (int i = 0; i < 13; i++) {
            old=ne;
            ne=arr[i];
            if(ne+old==target){
                System.out.println("position is"+i+"and"+(i-1));
                System.out.println("found");
            }


            
        }

    }
}