#include<stdio.h>
void main(){

    int a=12;
    printf("no>%d \n",a);
    int *p= &a;
    printf("ad>%p\n",&a);
    printf("po>%d\n",*p);  //use * to print min values
    scanf("%c",a);
}