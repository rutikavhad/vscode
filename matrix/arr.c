#include<stdio.h>

int main(){

    int counter=0;
    int k=0;
    int target=15;
    int i;
    int arr[]={1,2,3,4,5,6,7,8,9,10};


    for(i=0;i<10;i++){
        if(target!=counter){
            if(counter<target){
                counter=counter+arr[i];
            }
            else{
                counter=counter-arr[k];
                k++;

            }


        }
        else{
        printf("found\n");
        counter=counter+arr[i];
        }
    }
}