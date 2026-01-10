#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int array[8];
extern int flag;

/* globals filled by encode_sib_from_operand_and_modrm */
unsigned char generated_modrm = 0;
unsigned char generated_sib = 0;
int generated_disp_size = 0;
unsigned char generated_disp[4] = {0};
//use for genrate a SIB code for registers
int regg(char reg[4],int flag1){
    if(strcmp(reg,"eax")==0){
        if(flag1==0){ array[0]=0;array[1]=0;array[2]=0; }
        else{ array[3]=0;array[4]=0;array[5]=0; }
    }
    else if(strcmp(reg,"ecx")==0){
        if(flag1==0){ array[0]=0;array[1]=0;array[2]=1; }
        else{ array[3]=0;array[4]=0;array[5]=1; }
    }
    else if(strcmp(reg,"edx")==0){
        if(flag1==0){ array[0]=0;array[1]=1;array[2]=0; }
        else{ array[3]=0;array[4]=1;array[5]=0; }
    }
    else if(strcmp(reg,"ebx")==0){
        if(flag1==0){ array[0]=0;array[1]=1;array[2]=1; }
        else{ array[3]=0;array[4]=1;array[5]=1; }
    }
    else if(strcmp(reg,"esp")==0){
        if(flag1==0){ array[0]=1;array[1]=0;array[2]=0; }
        else{ array[3]=1;array[4]=0;array[5]=0; }
    }
    else if(strcmp(reg,"ebp")==0){
        if(flag1==0){ array[0]=1;array[1]=0;array[2]=1; }
        else{ array[3]=1;array[4]=0;array[5]=1; }
    }
    else if(strcmp(reg,"esi")==0){
        if(flag1==0){ array[0]=1;array[1]=1;array[2]=0; }
        else{ array[3]=1;array[4]=1;array[5]=0; }
    }
    else if(strcmp(reg,"edi")==0){
        if(flag1==0){ array[0]=1;array[1]=1;array[2]=1; }
        else{ array[3]=1;array[4]=1;array[5]=1; }
    }
    return 0;
}

int basse(int num){ //this for calculate base of SIB
    switch(num){
        case 1: return 0;
        case 2: return 1;
        case 4: return 2;
        case 8: return 3;
    }
    return -1;
}

int binary(){ // calculate binary code and hexa code
    unsigned int number=0;
    unsigned int number1=0;

    if(array[7]==1) number=1;

    unsigned int dd=6;
    unsigned int binaryv=2;

    for(int i=0;i<3;i++){
        if(array[dd]==1) number += binaryv;
        binaryv*=2;
        dd--;
    }

    if(array[3]==1) number1=1;

    dd--;
    binaryv=2;

    for(int i=0;i<3;i++){
        if(array[dd]==1) number1 += binaryv;
        binaryv*=2;
        dd--;
    }

    printf("SIB Hex = %X%X\n",number1,number);
    return 0;
}

//New function for calculate like this data as sib + modrm + r32 number (11) {mov eax, [esp + edi*8 + 12345678]}

unsigned char encode_sib_from_operand_and_modrm(const char *operand_in, const char *dest_reg){
 
    generated_modrm = 0;
    generated_sib = 0;
    generated_disp_size = 0;
    generated_disp[0]=generated_disp[1]=generated_disp[2]=generated_disp[3]=0;

    char operand[256];
    strncpy(operand, operand_in, sizeof(operand)-1);
    operand[sizeof(operand)-1]=0;
    char *start = strchr(operand,'[');
    char *end = strchr(operand,']');
    char inner[128];
    if(start && end){
        size_t len = end - start - 1;
        if(len >= sizeof(inner)) len = sizeof(inner)-1;
        strncpy(inner, start+1, len);
        inner[len]=0;
    } else {
        strncpy(inner, operand, sizeof(inner)-1);
        inner[sizeof(inner)-1]=0;
    }

    char tmp[128];
    strcpy(tmp, inner);
    char *tok = strtok(tmp, " +*");
    char reg1[4] = {0}, reg2[4] = {0};
    int regCount = 0;
    int scale = 1;
    long disp = 0;
    int have_disp = 0;

    while(tok){
        if(strlen(tok)==3){
            if(regCount==0) strcpy(reg1, tok);
            else strcpy(reg2, tok);
            regCount++;
        } else {
            long v = atol(tok);
            if(v==1 || v==2 || v==4 || v==8){
                scale = (int)v;
            } else {
                disp = v;
                have_disp = 1;
            }
        }
        tok = strtok(NULL, " +*");
    }

    if(regCount==0){
        reg1[0]=reg2[0]='\0';
        strcpy(reg1,"eax");
        strcpy(reg2,"eax");
    } else if(regCount==1){
        strcpy(reg2,"eax");
    }

    regg(reg1,0);
    regg(reg2,1);

    //compute SIB
    int index_reg = -1;
    int base_reg = -1;
    if(strcmp(reg1,"eax")==0) base_reg = 0;
    else if(strcmp(reg1,"ecx")==0) base_reg = 1;
    else if(strcmp(reg1,"edx")==0) base_reg = 2;
    else if(strcmp(reg1,"ebx")==0) base_reg = 3;
    else if(strcmp(reg1,"esp")==0) base_reg = 4;
    else if(strcmp(reg1,"ebp")==0) base_reg = 5;
    else if(strcmp(reg1,"esi")==0) base_reg = 6;
    else if(strcmp(reg1,"edi")==0) base_reg = 7;

    if(strcmp(reg2,"eax")==0) index_reg = 0;
    else if(strcmp(reg2,"ecx")==0) index_reg = 1;
    else if(strcmp(reg2,"edx")==0) index_reg = 2;
    else if(strcmp(reg2,"ebx")==0) index_reg = 3;
    else if(strcmp(reg2,"esp")==0) index_reg = 4;
    else if(strcmp(reg2,"ebp")==0) index_reg = 5;
    else if(strcmp(reg2,"esi")==0) index_reg = 6;
    else if(strcmp(reg2,"edi")==0) index_reg = 7;

    int scale_bits = basse(scale);
    if(scale_bits<0) scale_bits = 0;

    //for displacement size
    int disp_size = 0;
    if(have_disp){
        long v = disp;
        if(v >= -128 && v <= 127) disp_size = 1;
        else disp_size = 4;
    } else {
        disp_size = 0;
    }

    // special-case for ebp 5
    if(base_reg==5 && disp_size==0){
        disp_size = 4;
        have_disp = 0;
        disp = 0;
    }

    // build SIB byte: scale(2) index(3) base(3) 
    unsigned char sib = (unsigned char)((scale_bits<<6) | ((index_reg & 7)<<3) | (base_reg & 7));
    generated_sib = sib;

    int regfield = 0;
    if(strcmp(dest_reg,"eax")==0) regfield=0;
    else if(strcmp(dest_reg,"ecx")==0) regfield=1;
    else if(strcmp(dest_reg,"edx")==0) regfield=2;
    else if(strcmp(dest_reg,"ebx")==0) regfield=3;
    else if(strcmp(dest_reg,"esp")==0) regfield=4;
    else if(strcmp(dest_reg,"ebp")==0) regfield=5;
    else if(strcmp(dest_reg,"esi")==0) regfield=6;
    else if(strcmp(dest_reg,"edi")==0) regfield=7;

    
    int modbits = 0;
    if(disp_size==0) modbits = 0;
    else if(disp_size==1) modbits = 1;
    else modbits = 2;

    
    int rm = 4;
    unsigned char modrm = (unsigned char)((modbits<<6) | ((regfield & 7)<<3) | (rm & 7));
    generated_modrm = modrm;

    //displacment as in little-endian
    generated_disp_size = 0;
    if(disp_size==1){
        long v = disp;
        generated_disp[0] = (unsigned char)(v & 0xFF);
        generated_disp_size = 1;
    } else if(disp_size==4){
        long v = disp;
        generated_disp[0] = (unsigned char)(v & 0xFF);
        generated_disp[1] = (unsigned char)((v>>8)&0xFF);
        generated_disp[2] = (unsigned char)((v>>16)&0xFF);
        generated_disp[3] = (unsigned char)((v>>24)&0xFF);
        generated_disp_size = 4;
    } else {
        generated_disp_size = 0;
    }

    
    binary();

    return generated_sib;
}
