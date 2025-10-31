
//import utils.Continous_sort.missing;

public class find_missing {
    public static int missing (int a[]){ //this for sorted array
        
        for(int i=1;i<a.length;i++){
            int old=a[i-1];
           if(old+1!=a[i]){
            System.out.println(old+1+"is missing");
           }
        }

        return 0;

    }
    static int unsortedmissing(int a[]){

        return 0;
    }
    public static void main(String[] args) {
        int a[]={3,3,4,5,6,9}; //6 is missing
        circulersort.circulersortt(a);
        //Continous_sort.themissing(a);
        missing(a);
        
    }
}
