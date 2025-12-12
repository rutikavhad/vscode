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

static void trim_trailing_spaces(char *p){
    char *t = p + strlen(p) - 1;
    while(t >= p && isspace((unsigned char)*t)){ *t = 0; t--; }
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

    int section = 0; // 0=text 1=data 2=bss

    while(fgets(buffer, sizeof(buffer), fp)){
        lineno++;

        char line[512];
        strncpy(line, buffer, sizeof(line)-1);
        line[sizeof(line)-1]=0;

        /* strip comments starting with ';' */
        char *comment = strchr(line, ';');
        if(comment) *comment = 0;

        /* strip newline */
        char *pnewline = strchr(line, '\n');
        if(pnewline) *pnewline = 0;

        /* trim leading spaces */
        char *s = line;
        while(isspace((unsigned char)*s)) s++;
        if(*s==0) continue;

        /* SECTION SELECT */
        if(strcmp(s, ".text")==0){ section=0; continue; }
        if(strcmp(s, ".data")==0){ section=1; continue; }
        if(strcmp(s, ".bss" )==0){ section=2; continue; }

        /* parse mnemonic/op1/op2 with label support (label: or label <space> directive) */
        char mnemonic[32]={0};
        char op1[256]={0}, op2[256]={0};
        int parts = 0;

        {
            /* make a working copy that has comments removed */
            char copy[512];
            strncpy(copy, s, sizeof(copy)-1);
            copy[sizeof(copy)-1]=0;

            /* get first token */
            char *tok = strtok(copy, " \t");
            if(tok){
                /* detect label with trailing ':' */
                size_t toklen = strlen(tok);
                int is_label = 0;
                if(toklen > 0 && tok[toklen-1] == ':') is_label = 1;
                else {
                    /* detect label without colon but followed immediately by spaces then ':' in original line */
                    char *after = s + strlen(tok);
                    while(isspace((unsigned char)*after)) after++;
                    if(*after == ':') is_label = 1;
                }

                if(is_label){
                    /* find colon in original string and move past it */
                    char *colon = strchr(s, ':');
                    if(colon){
                        char *rest = colon + 1;
                        while(isspace((unsigned char)*rest)) rest++;
                        if(*rest){
                            /* copy rest to temp and tokenize */
                            char tmp_rest[512];
                            strncpy(tmp_rest, rest, sizeof(tmp_rest)-1);
                            tmp_rest[sizeof(tmp_rest)-1]=0;
                            char *t2 = strtok(tmp_rest, " \t");
                            if(t2){
                                strncpy(mnemonic, t2, sizeof(mnemonic)-1);
                                mnemonic[sizeof(mnemonic)-1]=0;
                                char *rest2 = rest + strlen(t2);
                                while(isspace((unsigned char)*rest2)) rest2++;
                                if(*rest2){
                                    char *comma = strchr(rest2, ',');
                                    if(comma){
                                        size_t len1 = comma - rest2;
                                        if(len1 >= sizeof(op1)) len1 = sizeof(op1)-1;
                                        strncpy(op1, rest2, len1); op1[len1]=0;
                                        char *p2 = comma + 1;
                                        while(isspace((unsigned char)*p2)) p2++;
                                        strncpy(op2, p2, sizeof(op2)-1);
                                        op2[sizeof(op2)-1]=0;
                                        parts = 2;
                                    } else {
                                        strncpy(op1, rest2, sizeof(op1)-1);
                                        op1[sizeof(op1)-1]=0;
                                        parts = 1;
                                    }
                                }
                            }
                        }
                    } else {
                        /* fallback: treat as empty directive */
                        mnemonic[0]=0;
                    }
                } else {
                    /* first token is mnemonic/directive or label-without-colon (handled below) */
                    strncpy(mnemonic, tok, sizeof(mnemonic)-1);
                    mnemonic[sizeof(mnemonic)-1]=0;
                    char *rest = s + strlen(tok);
                    while(isspace((unsigned char)*rest)) rest++;
                    if(*rest){
                        char *comma = strchr(rest, ',');
                        if(comma){
                            size_t len1 = comma - rest;
                            if(len1 >= sizeof(op1)) len1 = sizeof(op1)-1;
                            strncpy(op1, rest, len1); op1[len1]=0;
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
        }

        /* trim trailing spaces from op1/op2 */
        trim_trailing_spaces(op1);
        trim_trailing_spaces(op2);

        /* ----- FIX: handle label WITHOUT colon, e.g. "msg db ..." ----- */
        /* If mnemonic is not a known directive/instruction and op1 is present, treat first token as a label */
        if(
            strcmp(mnemonic,"db")!=0 &&
            strcmp(mnemonic,"dw")!=0 &&
            strcmp(mnemonic,"dd")!=0 &&
            strcmp(mnemonic,"dq")!=0 &&
            strcmp(mnemonic,"dt")!=0 &&
            strcmp(mnemonic,"resb")!=0 &&
            strcmp(mnemonic,"resw")!=0 &&
            strcmp(mnemonic,"resd")!=0 &&
            strcmp(mnemonic,"resq")!=0 &&
            strcmp(mnemonic,"rest")!=0 &&
            strcmp(mnemonic,"mov")!=0 &&
            strcmp(mnemonic,"add")!=0 &&
            strcmp(mnemonic,"sub")!=0 &&
            strcmp(mnemonic,"xor")!=0 &&
            strcmp(mnemonic,"cmp")!=0 &&
            strcmp(mnemonic,"push")!=0 &&
            strcmp(mnemonic,"pop")!=0 &&
            strcmp(mnemonic,"inc")!=0 &&
            strcmp(mnemonic,"dec")!=0 &&
            strcmp(mnemonic,"mul")!=0 &&
            strcmp(mnemonic,"div")!=0 &&
            strcmp(mnemonic,"jmp")!=0 &&
            op1[0] != 0
        )
        {
            /* shift: mnemonic <- op1 ; op1 <- op2 */
            strncpy(mnemonic, op1, sizeof(mnemonic)-1);
            mnemonic[sizeof(mnemonic)-1]=0;
            if(op2[0] != 0){
                strncpy(op1, op2, sizeof(op1)-1);
                op1[sizeof(op1)-1]=0;
                op2[0]=0;
                parts = 1;
            } else {
                op1[0]=0;
                parts = 0;
            }
        }

        /* final trim */
        trim_trailing_spaces(mnemonic);
        trim_trailing_spaces(op1);
        trim_trailing_spaces(op2);

        /* ================= DATA SECTION ================= */
        if(section==1)
        {
            if(strcmp(mnemonic,"db")==0){
                char *p = strstr(s,"db");
                if(p) p += 2;
                else p = s;
                while(isspace((unsigned char)*p)) p++;
                char *tok = strtok(p,",");
                while(tok){
                    while(isspace((unsigned char)*tok)) tok++;
                    if(tok[0]=='"' || tok[0]=='\''){
                        char *q = tok+1;
                        while(*q && *q!='"' && *q!='\'')
                            fputc(*q++, fo);
                    } else {
                        int v = atoi(tok);
                        fputc((unsigned char)v, fo);
                    }
                    tok = strtok(NULL,",");
                }
                continue;
            }

            if(strcmp(mnemonic,"dw")==0){
                int v = atoi(op1);
                fputc(v&0xFF,fo);
                fputc((v>>8)&0xFF,fo);
                continue;
            }

            if(strcmp(mnemonic,"dd")==0){
                int v = atoi(op1);
                fwrite(&v,4,1,fo);
                continue;
            }

            if(strcmp(mnemonic,"dq")==0){
                long long v = atoll(op1);
                fwrite(&v,8,1,fo);
                continue;
            }

            /* Option B: require operand for dt */
            if(strcmp(mnemonic,"dt")==0){
                if(op1[0]==0){
                    /* no operand provided - skip (user requested Option B) */
                    continue;
                } else {
                    /* write size specified by operand (if reasonable) */
                    int count = atoi(op1);
                    if(count <= 0) count = 10; /* fallback */
                    unsigned char z = 0;
                    for(int i=0;i<count;i++) fputc(z, fo);
                }
                continue;
            }
        }

        /* ================= BSS SECTION ================= */
        if(section==2)
        {
            if(strcmp(mnemonic,"resb")==0){
                int n = atoi(op1);
                for(int i=0;i<n;i++) fputc(0,fo);
                continue;
            }

            if(strcmp(mnemonic,"resw")==0){
                int n = atoi(op1) * 2;
                for(int i=0;i<n;i++) fputc(0,fo);
                continue;
            }

            if(strcmp(mnemonic,"resd")==0){
                int n = atoi(op1) * 4;
                for(int i=0;i<n;i++) fputc(0,fo);
                continue;
            }

            if(strcmp(mnemonic,"resq")==0){
                int n = atoi(op1) * 8;
                for(int i=0;i<n;i++) fputc(0,fo);
                continue;
            }

            if(strcmp(mnemonic,"rest")==0){
                int n = atoi(op1) * 10;
                for(int i=0;i<n;i++) fputc(0,fo);
                continue;
            }
        }

        /* -------------------------------------------
                 EXISTING INSTRUCTION LOGIC (unchanged)
           ------------------------------------------- */

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

        /* ---------------- INSTRUCTIONS --------------- */

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
                outbytes[outcount++] = 0x8B;
                encode_sib_from_operand_and_modrm(op2, op1);
                outbytes[outcount++] = generated_modrm;
                outbytes[outcount++] = generated_sib;
                if(generated_disp_size>0){
                    for(int i=0;i<generated_disp_size;i++){
                        outbytes[outcount++] = generated_disp[i];
                    }
                }
            }
            else if(parts==2){
                outbytes[outcount++] = 0x89; 
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"add")==0){
            if(parts==2){
                outbytes[outcount++] = 0x01;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"sub")==0){
            if(parts==2){
                outbytes[outcount++] = 0x29;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"xor")==0){
            if(parts==2){
                outbytes[outcount++] = 0x31;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"cmp")==0){
            if(parts==2){
                outbytes[outcount++] = 0x39;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"push")==0){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x50 + r);
            }
        }
        else if(strcmp(mnemonic,"pop")==0){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x58 + r);
            }
        }
        else if(strcmp(mnemonic,"inc")==0){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x40 + r);
            }
        }
        else if(strcmp(mnemonic,"dec")==0){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) outbytes[outcount++] = (unsigned char)(0x48 + r);
            }
        }
        else if(strcmp(mnemonic,"mul")==0){
            if(parts==2){
                outbytes[outcount++] = 0x0F;
                outbytes[outcount++] = 0xAF;
                unsigned char modrm = modrm_encode_regreg(op2, op1); 
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"div")==0){
            if(parts==2){
                outbytes[outcount++] = 0xF7;
                unsigned char modrm = modrm_encode_regreg(op1, op2);
                outbytes[outcount++] = modrm;
            }
        }
        else if(strcmp(mnemonic,"jmp")==0){
            if(parts==1 && is_number_string(op1)){
                outbytes[outcount++] = 0xE9;
                int imm = atoi(op1);
                outcount += write_imm32(outbytes+outcount, imm);
            }
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
