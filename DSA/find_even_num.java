public class find_even_num {

    public static void main(String[] args) {
        int[] nums={129,34,5,4,555,88,35666,6,4,4};
        int count=0;

        System.out.println(findnum(nums));
    }

   static int findnum(int[] nums){
    int count =0;
    for (int num : nums) {
        if(even(num)){
            count++;
        }
        
    }
    return count;
   }

   static boolean even(int num){
    int numbers=digits(num);
    return numbers % 2 ==0;
   }

   static int digits(int num){
   if(num<0){
    num=num * -1;
   }
   if(num==0){
    return 1;
   }
   int count =0;
   while(num>0){
    count++;
    num=num/10;
   }
    return count;
   }
}