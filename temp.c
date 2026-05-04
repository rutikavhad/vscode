#include<stdio.h>
void main(){
    printf("hello\n");
    int *p = (int*)0x7ffe0dd26e04;
    printf("%d", *p);


}