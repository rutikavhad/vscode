#include<stdio.h>
int array[8]={1,1,1,1,1,1,1,1};
void main(){
int a[]={0,0,1,0};
    int size=4;
	unsigned int number=0;
	unsigned int binary=2;
	unsigned int i=0;
	unsigned int dd=size-2;
    printf("%d",size);
	printf("the binary number is \n");

	if(a[size-1]==1){
	
		number=1;
	}
	while(i<size){
		printf("%d",a[i]);
		i++;
	}
	i=0;

	while(i<size-1){
		
		if(a[dd]==1){	number=number+binary;
			
		}
			binary=binary*2;
		dd--;
		i++;
	}//
	printf("\nthe Whole  number is : %d\n",number);

}