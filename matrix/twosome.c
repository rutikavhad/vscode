#include<stdio.h>

int givetwosome(int target){

    int arr[10]={12,34,54,65,7,8,87,56,4,23};

    int j=1,i=0;
    int cound=0;
    int flag=0;
  for(i=0;i<10;i++)
    {
        for(j=i;j<10;j++)
        {
            cound++;
            printf("%d\n",arr[i]+arr[j]);
            // if (arr[i]+arr[j]==target)
            // {
            // flag=1;
            // //printf("\n%d",target);
            // return target;
                
            // }
            
        }
        
        
    }
    return cound;
//     if (flag==0)
//     {
//     return -1;  
//   }

}

int main(){
    int target=15;
    printf("hello %d", givetwosome(target));
   

}