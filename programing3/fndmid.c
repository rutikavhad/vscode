#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define size 1000000
int array[size];
void main(){
 int j;
    srand(time(NULL));
   
    for (int i = 0; i < size; i++)
    {
        j=rand();
        array[i]=j;
       // printf("%d\n",array[i]);
    }
    int min=array[0];
    int max=array[0];

    //find a mid number form unsorted array but without sorting
    int midnum=size/2;



    int k=0;
    for (int i = 0; i < size; i++)
    {
        int fivedev[size];
        if (array[i]%5==0)
        { 
            fivedev[k]=array[i];
            k++;
            /* code */
        }
        
        if (min>array[i])

        {
            min=array[i];
            /* code */
        }
        else if(max<array[i]){
            max=array[i];
            }
            printf("%d\n",fivedev[i]);
        }    
        printf("min:%d,\n max:%d",min,max);
    
    

}