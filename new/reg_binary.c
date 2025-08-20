#include<stdlib.h>
#include<stdio.h>
#include<string.h>
int array[8];
int re1;
int flag=0;
int main(){
    
    char reg1[4];
    char reg2[4];
    printf("enter 1st & 2d registers\n");
    scanf("%s%s",reg1,reg2);
    int w=0;
    char reg[4];
    strcpy(reg, reg1);
   //this for register to binary
    while(w<=1){
        //eax=000;
    if (strcmp(reg, "eax") == 0 )
    {

    if (flag==0)
    {
        array[5]=0;
        array[6]=0;
        array[7]=0;
        flag=1;
    }
    else{
       
        array[2]=0;
        array[3]=0;
        array[4]=0;
    }
        
    }
    //ecx==001
    else if (strcmp(reg, "ecx") == 0 )
    {

    if (flag==0)
    {
        array[5]=0;
        array[6]=0;
        array[7]=1;
        flag=1;
    }
    else{
       
        array[2]=0;
        array[3]=0;
        array[4]=1;
    }
        
    }
    //edx==010
    else if (strcmp(reg, "edx") == 0 )
    {

    if (flag==0)
    {
        array[5]=0;
        array[6]=1;
        array[7]=0;
        flag=1;
    }
    else{
       
        array[2]=0;
        array[3]=1;
        array[4]=0;
    }
        
    }
    //ebx==011
    else if (strcmp(reg, "ebx") == 0 )
    {

    if (flag==0)
    {
        array[5]=0;
        array[6]=1;
        array[7]=1;
        flag=1;
    }
    else{
       
        array[2]=0;
        array[3]=1;
        array[4]=1;
    }
        
    }
    //esp==100
    else if (strcmp(reg, "esp") == 0 )
    {

    if (flag==0)
    {
        array[5]=1;
        array[6]=0;
        array[7]=0;
        flag=1;
    }
    else{
       
        array[2]=1;
        array[3]=0;
        array[4]=0;
    }
        
    }
    //ebp==101
    else if (strcmp(reg, "ebp") == 0 )
    {

    if (flag==0)
    {
        array[5]=1;
        array[6]=0;
        array[7]=1;
        flag=1;
    }
    else{
       
        array[2]=1;
        array[3]=0;
        array[4]=1;
    }
        
    }
    //esi==110
    else if (strcmp(reg, "esi") == 0 )
    {

    if (flag==0)
    {
        array[5]=1;
        array[6]=1;
        array[7]=0;
        flag=1;
    }
    else{
       
        array[2]=1;
        array[3]=1;
        array[4]=0;
    }
        
    }
    //edi=111
    else if (strcmp(reg, "edi") == 0 )
    {

    if (flag==0)
    {
        array[5]=1;
        array[6]=1;
        array[7]=1;
        flag=1;
    }
    else{
       
        array[2]=1;
        array[3]=1;
        array[4]=1;
    }
        
    }

    //this is for new register
     strcpy(reg, reg2);
    w++;
    }
    array[0]=array[1]=1;
   
    
    
   //this bianry done now move

   //binary to hexa

    int size=7;
	unsigned int number=0;
    int number1=0;
	unsigned int binary=2;
	unsigned int i=0;
	unsigned int dd=size-1;
	if(array[7]==1){
	
		number=1;
	}
	i=0;

	while(i<3){
		//printf("%d\n",array[dd]);
		if(array[dd]==1){	
            number=number+binary;
            
			
		}
			binary=binary*2;
		dd--;
		i++;
	}//


	printf("\nthe Whole  number is : %d\n",number);
//this for 2nd part

    if(array[3]==1){
	
		number1=1;
	}
	i=0;
    binary=2;
    dd=dd-1;
	while(i<3){
		//printf("%d\n",array[dd]);
		if(array[dd]==1){	
            number1=number1+binary;
			
		}
			binary=binary*2;
		dd--;
		i++;
	}
   printf("\nthe Whole  number is : %d\n",number1);

int temp;
temp =number1;
i=0;
while (i<=1)
{
    if (temp==10)
    {
        printf("\nA");
    }
else if(temp==11)
    {
        printf("\nB");
    }
    else if(temp==12)
    {
        printf("\nC");
    }
    else if(temp==13)
    {
        printf("\nD");
    }
    else if(temp==14)
    {
        printf("\nE");
    }
    else if(temp==15)
    {
        printf("\nF");
    }
    else
    printf("\t%d",temp);
    temp=number;
    i++;
}


return 0;
}