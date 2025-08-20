#include<stdio.h>
void main(){

    int c=2;
    int num=25;
    int temp=0;
    
    while(c<num)
    {
        /* code */
        if (num%c==0)
        {
            /* code */
            printf("number is not prime");
            break;
            temp=1;
        
        }
        else{
            c=c+1;

        }
        
    }
    if (temp=0)
    {
        printf("number is prime");
        /* code */
    }
    
    
}