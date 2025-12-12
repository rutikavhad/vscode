#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int array[8];
int flag=0;

unsigned char modrm_encode_regreg(const char *r1, const char *r2){

    flag = 0;

    char A[4], B[4], reg[4];
    strcpy(A,r1);
    strcpy(B,r2);
    strcpy(reg,A);

    int w=0;

    while(w<=1){ //code 000
        if(strcmp(reg,"eax")==0){
            if(flag==0){ array[5]=0;array[6]=0;array[7]=0; flag=1; }
            else{ array[2]=0;array[3]=0;array[4]=0; }
        }
        else if(strcmp(reg,"ecx")==0){//code 001
            if(flag==0){ array[5]=0;array[6]=0;array[7]=1; flag=1; }
            else{ array[2]=0;array[3]=0;array[4]=1; }
        }
        else if(strcmp(reg,"edx")==0){//code 010
            if(flag==0){ array[5]=0;array[6]=1;array[7]=0; flag=1; }
            else{ array[2]=0;array[3]=1;array[4]=0; }
        }
        else if(strcmp(reg,"ebx")==0){//code 011
            if(flag==0){ array[5]=0;array[6]=1;array[7]=1; flag=1; }
            else{ array[2]=0;array[3]=1;array[4]=1; }
        }
        else if(strcmp(reg,"esp")==0){//code 100
            if(flag==0){ array[5]=1;array[6]=0;array[7]=0; flag=1; }
            else{ array[2]=1;array[3]=0;array[4]=0; }
        }
        else if(strcmp(reg,"ebp")==0){//code 101
            if(flag==0){ array[5]=1;array[6]=0;array[7]=1; flag=1; }
            else{ array[2]=1;array[3]=0;array[4]=1; }
        }
        else if(strcmp(reg,"esi")==0){//code 110
            if(flag==0){ array[5]=1;array[6]=1;array[7]=0; flag=1; }
            else{ array[2]=1;array[3]=1;array[4]=0; }
        }
        else if(strcmp(reg,"edi")==0){//code 111
            if(flag==0){ array[5]=1;array[6]=1;array[7]=1; flag=1; }
            else{ array[2]=1;array[3]=1;array[4]=1; }
        }

        strcpy(reg,B);
        w++;
    }

    array[0]=1;
    array[1]=1;

    unsigned char final =
        (array[0]<<7)|(array[1]<<6)|(array[2]<<5)|(array[3]<<4)|
        (array[4]<<3)|(array[5]<<2)|(array[6]<<1)|array[7];

    printf("ModRM Hex = %02X\n",final);
    return final;
}
