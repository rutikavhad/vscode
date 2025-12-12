#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

int array[8];
int flag=0;


int modrm_main(){

    char reg1[4];
    char reg2[4];
    printf("enter 1st & 2d registers\n");
    scanf("%s%s",reg1,reg2);
    int w=0;
    char reg[4];
    strcpy(reg, reg1);

   //this for register to binary
    while(w<=1){

    if (strcmp(reg, "eax") == 0 ){
        if (flag==0){
            array[5]=0; array[6]=0; array[7]=0; flag=1;
        }
        else{ array[2]=0; array[3]=0; array[4]=0; }
    }
    else if (strcmp(reg, "ecx") == 0 ){
        if (flag==0){
            array[5]=0; array[6]=0; array[7]=1; flag=1;
        }
        else{ array[2]=0; array[3]=0; array[4]=1; }
    }
    else if (strcmp(reg, "edx") == 0 ){
        if (flag==0){
            array[5]=0; array[6]=1; array[7]=0; flag=1;
        }
        else{ array[2]=0; array[3]=1; array[4]=0; }
    }
    else if (strcmp(reg, "ebx") == 0 ){
        if (flag==0){
            array[5]=0; array[6]=1; array[7]=1; flag=1;
        }
        else{ array[2]=0; array[3]=1; array[4]=1; }
    }
    else if (strcmp(reg, "esp") == 0 ){
        if (flag==0){
            array[5]=1; array[6]=0; array[7]=0; flag=1;
        }
        else{ array[2]=1; array[3]=0; array[4]=0; }
    }
    else if (strcmp(reg, "ebp") == 0 ){
        if (flag==0){
            array[5]=1; array[6]=0; array[7]=1; flag=1;
        }
        else{ array[2]=1; array[3]=0; array[4]=1; }
    }
    else if (strcmp(reg, "esi") == 0 ){
        if (flag==0){
            array[5]=1; array[6]=1; array[7]=0; flag=1;
        }
        else{ array[2]=1; array[3]=1; array[4]=0; }
    }
    else if (strcmp(reg, "edi") == 0 ){
        if (flag==0){
            array[5]=1; array[6]=1; array[7]=1; flag=1;
        }
        else{ array[2]=1; array[3]=1; array[4]=1; }
    }

    strcpy(reg, reg2);
    w++;
    }

    array[0]=array[1]=1;

    //binary to hex
    int size=7;
    unsigned int number=0;
    int number1=0;
    unsigned int binary=2;
    unsigned int i=0;
    unsigned int dd=size-1;

    if(array[7]==1)
        number=1;

    i=0;
    while(i<3){
        if(array[dd]==1)
            number=number+binary;
        binary=binary*2;
        dd--;
        i++;
    }

    printf("\nHigh 3 bits number : %d\n",number);

    if(array[3]==1) number1=1;

    i=0;
    binary=2;
    dd=dd-1;
    while(i<3){
        if(array[dd]==1)
            number1=number1+binary;
        binary=binary*2;
        dd--;
        i++;
    }

    printf("Low 3 bits number : %d\n",number1);

    printf("Hex = %X%X\n",number1,number);
    return 0;
}



/*                  THIS FOR GET REGISTER BINARY NUMBER BY MENUALY                    */

int regg(char reg[4],int flag1){
    if (strcmp(reg, "eax") == 0 ){
        if(flag1==0){ array[0]=0;array[1]=0;array[2]=0; }
        else{ array[3]=0;array[4]=0;array[5]=0; }
    }
    else if (strcmp(reg, "ecx") == 0 ){
        if(flag1==0){ array[0]=0;array[1]=0;array[2]=1; }
        else{ array[3]=0;array[4]=0;array[5]=1; }
    }
    else if (strcmp(reg, "edx") == 0 ){
        if(flag1==0){ array[0]=0;array[1]=1;array[2]=0; }
        else{ array[3]=0;array[4]=1;array[5]=0; }
    }
    else if (strcmp(reg, "ebx") == 0 ){
        if(flag1==0){ array[0]=0;array[1]=1;array[2]=1; }
        else{ array[3]=0;array[4]=1;array[5]=1; }
    }
    else if (strcmp(reg, "esp") == 0 ){
        if(flag1==0){ array[0]=1;array[1]=0;array[2]=0; }
        else{ array[3]=1;array[4]=0;array[5]=0; }
    }
    else if (strcmp(reg, "ebp") == 0 ){
        if(flag1==0){ array[0]=1;array[1]=0;array[2]=1; }
        else{ array[3]=1;array[4]=0;array[5]=1; }
    }
    else if (strcmp(reg, "esi") == 0 ){
        if(flag1==0){ array[0]=1;array[1]=1;array[2]=0; }
        else{ array[3]=1;array[4]=1;array[5]=0; }
    }
    else if (strcmp(reg, "edi") == 0 ){
        if(flag1==0){ array[0]=1;array[1]=1;array[2]=1; }
        else{ array[3]=1;array[4]=1;array[5]=1; }
    }
    return 0;
}

int basse(int num){
    switch(num){
        case 1: return 0;
        case 2: return 1;
        case 4: return 2;
        case 8: return 3;
        default: return -1;
    }
}

int binary(){
    int size=7;
    unsigned int number=0;
    int number1=0;
    unsigned int binary=2;
    unsigned int i=0;
    unsigned int dd=size-1;

    if(array[7]==1)
        number=1;

    i=0;
    while(i<3){
        if(array[dd]==1)
            number=number+binary;
        binary=binary*2;
        dd--;
        i++;
    }

    if(array[3]==1) number1=1;
    i=0;
    binary=2;
    dd=dd-1;

    while(i<3){
        if(array[dd]==1)
            number1=number1+binary;
        binary=binary*2;
        dd--;
        i++;
    }

    printf("SIB Hex = %X%X\n",number1,number);
    return 0;
}

int sib_main(){
    char filepath[256];
    FILE *fp;
    char buffer[256], operand[128];
    char reg11[4], reg22[4], *start, *end, *token;
    int base, linenumber=0, regCount;

    printf("Enter .asm File Path: ");
    scanf("%s",filepath);
    fp=fopen(filepath,"r");

    while(fgets(buffer, sizeof(buffer), fp)){
        linenumber++;

        start=strchr(buffer,'[');
        end=strchr(buffer,']');

        if(start && end){
            reg11[0]=reg22[0]='\0';
            base=1;
            regCount=0;

            strncpy(operand, start+1, end-start-1);
            operand[end-start-1]='\0';

            token=strtok(operand," +*");

            while(token){
                if(strlen(token)==3){
                    if(regCount==0) strcpy(reg11,token);
                    else strcpy(reg22,token);

                    regCount++;
                }
                else{
                    base=atoi(token);
                }
                token=strtok(NULL," +*");
            }

            int f=0;
            regg(reg11,f);
            f=1;
            regg(reg22,f);

            int bass=basse(base);
            array[6]=bass&1;
            array[7]=(bass>>1)&1;

            binary();
        }
    }
    return 0;
}

/****************************************************
          NEW ASSEMBLER MAIN IN YOUR STYLE
*****************************************************/
int main(){

    char filepath[256];
    char outpath[256];
    FILE *fp,*fo;
    char buffer[256];
    int lineno=0;

    printf("Enter input asm file: ");
    scanf("%s",filepath);

    printf("Enter output bin file: ");
    scanf("%s",outpath);

    fp=fopen(filepath,"r");
    fo=fopen(outpath,"wb");

    while(fgets(buffer,sizeof(buffer),fp)){
        lineno++;

        char *movv=strstr(buffer,"mov");
        if(movv){

            char op1[32],op2[64];
            sscanf(buffer,"mov %[^,], %s",op1,op2);

            if(op2[0]=='['){
                // MEMORY → USE YOUR SIB CODE EXACTLY
                printf("\nLine %d: Memory MOV detected\n",lineno);

                // reuse same parsing from sib_main
                char *start=strchr(buffer,'[');
                char *end=strchr(buffer,']');
                char operand[128],*token;
                char r1[4],r2[4];
                int base=1,regCount=0;

                strncpy(operand,start+1,end-start-1);
                operand[end-start-1]='\0';

                token=strtok(operand," +*");
                while(token){
                    if(strlen(token)==3){
                        if(regCount==0) strcpy(r1,token);
                        else strcpy(r2,token);
                        regCount++;
                    }
                    else base=atoi(token);
                    token=strtok(NULL," +*");
                }

                int ff=0;
                regg(r1,ff);
                ff=1;
                regg(r2,ff);

                int bass=basse(base);
                array[6]=bass&1;
                array[7]=(bass>>1)&1;

                binary();

                unsigned char final = (array[0]<<7)|(array[1]<<6)|(array[2]<<5)|(array[3]<<4)|
                                      (array[4]<<3)|(array[5]<<2)|(array[6]<<1)|array[7];

                fwrite(&final,1,1,fo);
            }
            else{
                // REGISTER to REGISTER → use your modrm code
                printf("\nLine %d: Register MOV detected\n",lineno);

                // simulate your program1 internal logic
                char r1[4],r2[4];
                strcpy(r1,op1);
                strcpy(r2,op2);
                flag=0;

                char reg[4];
                char regA[4], regB[4];
                strcpy(regA, r1);
                strcpy(regB, r2);

                strcpy(reg, regA);

                int w=0;
                while(w<=1){

                    if (strcmp(reg, "eax") == 0 ){
                        if(flag==0){ array[5]=0;array[6]=0;array[7]=0; flag=1; }
                        else{ array[2]=0;array[3]=0;array[4]=0; }
                    }
                    else if (strcmp(reg, "ecx") == 0 ){
                        if(flag==0){ array[5]=0;array[6]=0;array[7]=1; flag=1; }
                        else{ array[2]=0;array[3]=0;array[4]=1; }
                    }
                    else if (strcmp(reg, "edx") == 0 ){
                        if(flag==0){ array[5]=0;array[6]=1;array[7]=0; flag=1; }
                        else{ array[2]=0;array[3]=1;array[4]=0; }
                    }
                    else if (strcmp(reg, "ebx") == 0 ){
                        if(flag==0){ array[5]=0;array[6]=1;array[7]=1; flag=1; }
                        else{ array[2]=0;array[3]=1;array[4]=1; }
                    }
                    else if (strcmp(reg, "esp") == 0 ){
                        if(flag==0){ array[5]=1;array[6]=0;array[7]=0; flag=1; }
                        else{ array[2]=1;array[3]=0;array[4]=0; }
                    }
                    else if (strcmp(reg, "ebp") == 0 ){
                        if(flag==0){ array[5]=1;array[6]=0;array[7]=1; flag=1; }
                        else{ array[2]=1;array[3]=0;array[4]=1; }
                    }
                    else if (strcmp(reg, "esi") == 0 ){
                        if(flag==0){ array[5]=1;array[6]=1;array[7]=0; flag=1; }
                        else{ array[2]=1;array[3]=1;array[4]=0; }
                    }
                    else if (strcmp(reg, "edi") == 0 ){
                        if(flag==0){ array[5]=1;array[6]=1;array[7]=1; flag=1; }
                        else{ array[2]=1;array[3]=1;array[4]=1; }
                    }

                    strcpy(reg,regB);
                    w++;
                }

                array[0]=array[1]=1;

                unsigned char final=(array[0]<<7)|(array[1]<<6)|(array[2]<<5)|(array[3]<<4)|
                                     (array[4]<<3)|(array[5]<<2)|(array[6]<<1)|array[7];

                printf("ModRM Hex = %02X\n",final);
                fwrite(&final,1,1,fo);
            }
        }
    }

    fclose(fp);
    fclose(fo);

    printf("\nAssembling Done.\n");

    return 0;
}
