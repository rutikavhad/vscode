/*read asm → parse → identify instruction → build bytes → print hex → write to bin file
use this mymoderm.c and sib.c file to calculate sib.c modifyed for dis32 number in sib
main.c can calculate instructions IA-32 format (mov,add,sub,etc ) not all around 12 instructions most common*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

extern unsigned char modrm_encode_regreg(const char *r1, const char *r2);

// from sib.c 
extern unsigned char generated_modrm;
extern unsigned char generated_sib;
extern int generated_disp_size;
extern unsigned char generated_disp[4];
extern unsigned char encode_sib_from_operand_and_modrm(const char *operand, const char *dest_reg);

// helper:register name to reg-id (0..7) 
int reg_index(const char *r){
    if(strcmp(r,"eax")==0) return 0;
    if(strcmp(r,"ecx")==0) return 1;
    if(strcmp(r,"edx")==0) return 2;
    if(strcmp(r,"ebx")==0) return 3;
    if(strcmp(r,"esp")==0) return 4;
    if(strcmp(r,"ebp")==0) return 5;
    if(strcmp(r,"esi")==0) return 6;
    if(strcmp(r,"edi")==0) return 7;
    return -1;
}

// write little-endian 32-bit
int write_imm32(unsigned char *buf, int value){
    buf[0] = (unsigned char)(value & 0xFF);
    buf[1] = (unsigned char)((value >> 8) & 0xFF);
    buf[2] = (unsigned char)((value >> 16) & 0xFF);
    buf[3] = (unsigned char)((value >> 24) & 0xFF);
    return 4;
}

//for hex format
void format_hex(unsigned char *bytes, int n, char *out, int outsz){
    out[0]=0;
    char tmp[8];
    for(int i=0;i<n;i++){
        snprintf(tmp,sizeof(tmp),"%02X", bytes[i]);
        strncat(out,tmp,outsz - strlen(out) - 1);
        if(i < n-1) strncat(out," ", outsz - strlen(out) - 1);
    }
}

int is_number_string(const char *s){
    if(!s || !s[0]) return 0;
    int i=0;
    if(s[0]=='-' || s[0]=='+') i=1;
    for(; s[i]; ++i){
        if(!isdigit((unsigned char)s[i])) return 0;
    }
    return 1;
}

int main(){ // read data form .asm file
    char filepath[256];
    char outpath[256];
    FILE *fp,*fo;
    char buffer[512];
    int lineno=0;

    printf("Enter input asm file: ");
    scanf("%255s",filepath);

    printf("Enter output bin file: ");
    scanf("%255s",outpath);

    fp = fopen(filepath,"r");
    if(!fp){ perror("fopen input"); return 1; }
    fo = fopen(outpath,"wb");
    if(!fo){ perror("fopen output"); fclose(fp); return 1; }

    while(fgets(buffer, sizeof(buffer), fp)){
        lineno++;
        
        char line[512];
        strncpy(line, buffer, sizeof(line)-1);
        line[sizeof(line)-1]=0;
        char *pnewline = strchr(line, '\n');
        if(pnewline) *pnewline = 0;
        //for empty lines
        char *s=line;
        while(isspace((unsigned char)*s)) s++;
        if(*s==0) continue;
        if(s[0]==';') continue;

      //genrate token for each instruction
        char mnemonic[16]={0};
        char op1[128]={0}, op2[128]={0};
        int parts = 0;
        {
            char copy[512];
            strcpy(copy, s);
            char *tok = strtok(copy, " \t");
            if(tok){
                strncpy(mnemonic, tok, sizeof(mnemonic)-1);
                char *rest = s + strlen(tok);
                while(isspace((unsigned char)*rest)) rest++;
                if(*rest){
                    char *comma = strchr(rest, ',');
                    if(comma){
                        size_t len1 = comma - rest;
                        while(len1 && isspace((unsigned char)rest[len1-1])) len1--;
                        strncpy(op1, rest, (len1 < sizeof(op1)-1)? len1: sizeof(op1)-1);
                        op1[(len1 < sizeof(op1)-1)? len1: sizeof(op1)-1]=0;
                        char *p2 = comma + 1;
                        while(isspace((unsigned char)*p2)) p2++;
                        strncpy(op2, p2, sizeof(op2)-1);
                        op2[sizeof(op2)-1]=0;
                        parts = 2;
                    } else {
                        strncpy(op1, rest, sizeof(op1)-1);
                        op1[sizeof(op1)-1]=0;
                        parts = 1;
                    }
                }
            }
        }

        // trim operands
        {
            char *t;
            while(op1[0] && isspace((unsigned char)op1[0])) memmove(op1, op1+1, strlen(op1));
            t = op1 + strlen(op1) - 1;
            while(t>=op1 && isspace((unsigned char)*t)){ *t=0; t--; }
            while(op2[0] && isspace((unsigned char)op2[0])) memmove(op2, op2+1, strlen(op2));
            t = op2 + strlen(op2) - 1;
            while(t>=op2 && isspace((unsigned char)*t)){ *t=0; t--; }
        }

        unsigned char outbytes[16];
        int outcount = 0;

        // FOR MOV
        if(strcmp(mnemonic,"mov")==0){
            if(parts==2 && is_number_string(op2)){
                int rd = reg_index(op1);
                if(rd>=0){
                    outbytes[outcount++] = (unsigned char)(0xB8 + rd);
                    int imm = atoi(op2);
                    outcount += write_imm32(outbytes+outcount, imm);
                }
            }
            else if(parts==2 && op2[0]=='['){
                //THIS FOR MEMORY + SIB+ r32
                outbytes[outcount++] = 0x8B;\
                //CALL SIB CODE
                encode_sib_from_operand_and_modrm(op2, op1); 
                //MODRM FOR SIB 100
                outbytes[outcount++] = generated_modrm;
                outbytes[outcount++] = generated_sib;
                if(generated_disp_size>0){
                    for(int i=0;i<generated_disp_size;i++){
                        outbytes[outcount++] = generated_disp[i];
                    }
                }
            }
            else if(parts==2){ //this also MOV reg32 and r32
                outbytes[outcount++] = 0x89; 
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
            else {
            }
        }
        else if(strcmp(mnemonic,"add")==0){ // this for ADD
            if(parts==2){
                outbytes[outcount++] = 0x01;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"sub")==0){// this for SUB
            if(parts==2){
                outbytes[outcount++] = 0x29;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"xor")==0){ // this for XOR
            if(parts==2){
                outbytes[outcount++] = 0x31;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"cmp")==0){// this for CMP
            if(parts==2){
                outbytes[outcount++] = 0x39;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"push")==0){// this for PUSH
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x50 + r);
            }
        }
        else if(strcmp(mnemonic,"pop")==0){// thi for POP
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x58 + r);
            }
        }
        else if(strcmp(mnemonic,"inc")==0){//this for INC
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x40 + r);
            }
        }
        else if(strcmp(mnemonic,"dec")==0){//this for DEC
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x48 + r);
            }
        }
        else if(strcmp(mnemonic,"mul")==0){//this for MUL
            if(parts==2){
                outbytes[outcount++] = 0x0F;
                outbytes[outcount++] = 0xAF;
                unsigned char modrm = modrm_encode_regreg(op2, op1); 
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"div")==0){ // this for DIV
            if(parts==2){
                outbytes[outcount++] = 0xF7;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"jmp")==0){//this for JMP
            if(parts==1 && is_number_string(op1)){
                outbytes[outcount++] = 0xE9;
                int imm = atoi(op1);
                outcount += write_imm32(outbytes+outcount, imm);
            }
        }
        else {
        }

        if(outcount>0){
            fwrite(outbytes,1,outcount,fo);
            char hexout[256];
            format_hex(outbytes,outcount,hexout,sizeof(hexout));
            printf("%-24s %s\n", hexout, s);
        }
    }

    fclose(fp);
    fclose(fo);

    printf("\nAssembling Done.\n");
    return 0;
}
