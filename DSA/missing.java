class missing {


  
    public static int missingNumber(int[] nums) {
        int number=0;
        int i=0;
        while(i<nums.length){
            int correct=nums[i]-1;
            if(nums[i]!=nums[correct]){
                int temp=nums[correct];
                nums[correct]=nums[i];
                nums[i]=temp;
            }
            else{
                number=nums[i];
                i++;
                
            }

        }
        return number;
    }


    public static void main(String[] args) {

        int[] nums={3,0,1};
        missingNumber(nums);
        
    }
}