/* - labels stored in arrays
   - supports db/dw/dd/dq/resb/resd/resq/rest
   - supports mov reg, imm ; mov reg, reg ; mov reg, [symbol] ; mov reg, [reg+reg*scale+disp]
   - supports add/sub/xor/cmp/push/pop/inc/dec/mul/div/jmp/int
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "databss.h"

// externs for modrm.c and sib.c 
extern unsigned char modrm_encode_regreg(const char *r1, const char *r2);
extern unsigned char encode_sib_from_operand_and_modrm(const char *operand, const char *dest_reg);
extern unsigned char generated_modrm;
extern unsigned char generated_sib;
extern int generated_disp_size;
extern unsigned char generated_disp[4];

// simple label table
#define MAX_LABELS 1024
char labels_name[MAX_LABELS][64];
unsigned long labels_addr[MAX_LABELS];
int labels_count = 0;

int find_label(const char *name){
    if(!name) return -1;
    for(int i=0;i<labels_count;i++){
        if(strcmp(labels_name[i], name)==0) return i;
    }
    return -1;
}
void add_label(const char *name, unsigned long addr){
    if(find_label(name) >= 0) return;
    if(labels_count < MAX_LABELS){
        strncpy(labels_name[labels_count], name, sizeof(labels_name[0])-1);
        labels_name[labels_count][sizeof(labels_name[0])-1] = 0;
        labels_addr[labels_count] = addr;
        labels_count++;
    }
}

// utilities
static void trim(char *s){
    if(!s) return;
    while(*s && isspace((unsigned char)*s)) memmove(s, s+1, strlen(s));
    int n = strlen(s);
    while(n>0 && isspace((unsigned char)s[n-1])) s[--n] = 0;
}
int is_register(const char *s){
    if(!s) return 0;
    return !strcmp(s,"eax")||!strcmp(s,"ebx")||!strcmp(s,"ecx")||!strcmp(s,"edx")||
           !strcmp(s,"esi")||!strcmp(s,"edi")||!strcmp(s,"esp")||!strcmp(s,"ebp");
}
int reg_index(const char *r){
    if(!r) return -1;
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
int is_number_string(const char *s){
    if(!s||!s[0]) return 0;
    int i=0; if(s[0]=='+'||s[0]=='-') i=1;
    if(s[i]=='0' && (s[i+1]=='x' || s[i+1]=='X')) i += 2;
    for(; s[i]; ++i) if(!isxdigit((unsigned char)s[i])) return 0;
    return 1;
}
long parse_number(const char *s){
    if(!s) return 0;
    return strtol(s, NULL, 0);
}

//print output
void print_ndisasm_line(unsigned long addr, unsigned char *bytes, int n, const char *src){
    printf("%08lX  ", addr);
    for(int i=0;i<n;i++) printf("%02X", bytes[i]);
    if(n < 6){
        int pad = (6 - n) * 2;
        for(int i=0;i<pad;i++) putchar(' ');
    }
    printf("   %s\n", src);
}

//work as one pass
enum section_t { SEC_TEXT=0, SEC_DATA=1, SEC_BSS=2 };

#define MAX_LINES 8192
char *lines_store[MAX_LINES];
enum section_t lines_sec[MAX_LINES];
unsigned long lines_addr[MAX_LINES];
int lines_count = 0;

void store_line(const char *txt, enum section_t sec, unsigned long addr){
    if(lines_count >= MAX_LINES) return;
    lines_store[lines_count] = strdup(txt);
    lines_sec[lines_count] = sec;
    lines_addr[lines_count] = addr;
    lines_count++;
}

// simple helper: estimate bytes for a single source line
int estimate_bytes(const char *mn, const char *op1, const char *op2){
    if(!mn || !mn[0]) return 0;
    if(!strcmp(mn,"mov")){
        if(op2 && op2[0]=='[') return 1 + 1 + 1 + 4; //opcode + modrm + sib + disp32
        if(op2 && (is_number_string(op2) || (!is_register(op2) && isalpha((unsigned char)op2[0])))) return 1 + 4;
        return 1 + 1;
    }
    if(!strcmp(mn,"add")||!strcmp(mn,"sub")||!strcmp(mn,"xor")||!strcmp(mn,"cmp")) return 1 + 1;
    if(!strcmp(mn,"push")||!strcmp(mn,"pop")||!strcmp(mn,"inc")||!strcmp(mn,"dec")) return 1;
    if(!strcmp(mn,"mul")) return 2 + 1;
    if(!strcmp(mn,"div")) return 1 + 1;
    if(!strcmp(mn,"jmp")) return 1 + 4;
    if(!strcmp(mn,"int")) return 2;
    return 0;
}


void split_mnemonic_rest(const char *line, char *mn, char *rest){
    mn[0]=0; rest[0]=0;
    if(!line) return;
    char tmp[1024]; strncpy(tmp, line, sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0;
    trim(tmp);
    // remove comments
    char *c = strchr(tmp,';'); if(c) *c = 0;
    trim(tmp);
    if(tmp[0]==0) return;
    // tokenise
    char *p = tmp;
    while(*p && isspace((unsigned char)*p)) p++;
    char *q = p;
    while(*q && !isspace((unsigned char)*q)) q++;
    if(*q) { *q = 0; q++; while(*q && isspace((unsigned char)*q)) q++; }
    strncpy(mn,p,64-1); mn[63]=0;
    if(q) { strncpy(rest,q,512-1); rest[511]=0; trim(rest); }
}

//split operands by comma
int split_operands(const char *rest, char *op1, char *op2){
    op1[0]=0; op2[0]=0;
    if(!rest || !rest[0]) return 0;
    char tmp[512]; strncpy(tmp, rest, sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0;
    char *c = strchr(tmp, ',');
    if(c){
        *c = 0;
        strncpy(op1, tmp, 255); op1[255]=0; trim(op1);
        strncpy(op2, c+1, 255); op2[255]=0; trim(op2);
        return 2;
    } else {
        strncpy(op1, tmp, 255); op1[255]=0; trim(op1);
        return 1;
    }
}

// pass1: read file, collect labels and compute addresses
int pass1(const char *fname){
    FILE *f = fopen(fname,"r");
    if(!f){ perror("fopen"); return 0; }
    char buf[1024];
    enum section_t sec = SEC_TEXT;
    unsigned long addr = 0;
    int lineno = 0;
    while(fgets(buf,sizeof(buf),f)){
        lineno++;
        char line[1024]; strncpy(line, buf, sizeof(line)-1); line[sizeof(line)-1]=0;
        char *pn = strchr(line, '\n'); if(pn) *pn=0;
        trim(line);
        if(!line[0]) continue;
        if(line[0]==';') continue;
        
        if(!strcmp(line,"section .data") || !strcmp(line,".data")){ sec = SEC_DATA; continue; }
        if(!strcmp(line,"section .bss") || !strcmp(line,".bss")){ sec = SEC_BSS; continue; }
        if(!strcmp(line,"section .text") || !strcmp(line,".text")){ sec = SEC_TEXT; continue; }
        // label
        char copy[1024]; strncpy(copy,line,sizeof(copy)-1); copy[sizeof(copy)-1]=0;
        char *tok = strtok(copy," \t");
        if(tok && tok[strlen(tok)-1]==':'){
            tok[strlen(tok)-1]=0; 
            add_label(tok, addr);
            store_line(line, sec, addr);//store for ptint
            continue;
        }
        
        char mn[64], rest[512]; split_mnemonic_rest(line, mn, rest);
        if(sec == SEC_DATA && ( !strcmp(mn,"db") || !strcmp(mn,"dw")||!strcmp(mn,"dd")||!strcmp(mn,"dq")||!strcmp(mn,"dt") )){
            long sz = process_data_directive_size_simple(mn, rest);
            store_line(line, sec, addr);
            addr += (unsigned long)sz;
            continue;
        }
        if(sec == SEC_BSS && ( !strcmp(mn,"resb")||!strcmp(mn,"resw")||!strcmp(mn,"resd")||!strcmp(mn,"resq")||!strcmp(mn,"rest") )){
            long sz = process_data_directive_size_simple(mn, rest);
            store_line(line, sec, addr);
            addr += (unsigned long)sz;
            continue;
        }
        // instruction
        char op1[256], op2[256]; op1[0]=0; op2[0]=0;
        split_operands(rest, op1, op2);
        int est = estimate_bytes(mn, op1, op2);
        store_line(line, sec, addr);
        addr += (unsigned long)est;
    }
    fclose(f);
    return 1;
}

// this will work as two pass
int write_imm32(unsigned char *buf, unsigned long v){
    buf[0] = v & 0xFF;
    buf[1] = (v>>8)&0xFF;
    buf[2] = (v>>16)&0xFF;
    buf[3] = (v>>24)&0xFF;
    return 4;
}

void write_and_print(FILE *fo, unsigned long addr, unsigned char *buf, int n, const char *src){
    if(n>0) fwrite(buf,1,n,fo);
    print_ndisasm_line(addr, buf, n, src);
}

//this help to converter modrm + sib 
int encode_abs_mem(unsigned char *out, int regfield, unsigned long addr32){
    int idx = 0;
    unsigned char modrm = (unsigned char)((0<<6) | ((regfield & 7) << 3) | (4 & 7));
    out[idx++] = modrm;
    out[idx++] = 0x25; /* SIB = 0x25 */
    idx += write_imm32(out+idx, addr32);
    return idx;
}

// assemble stored lines
int pass2(const char *outpath){
    FILE *fo = fopen(outpath,"wb");
    if(!fo){ perror("fopen out"); return 0; }
    unsigned long addr = 0;
    for(int i=0;i<lines_count;i++){
        char *line = lines_store[i];
        enum section_t sec = lines_sec[i];
        addr = lines_addr[i];
        //skip commands
        char tmp[1024]; strncpy(tmp, line, sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0;
        trim(tmp);
        if(!tmp[0]) continue;
        if(tmp[0]==';') continue;
       
        
        char cp[1024]; strncpy(cp,tmp,sizeof(cp)-1); cp[sizeof(cp)-1]=0;
        char *first = strtok(cp," \t");
        if(first && first[strlen(first)-1]==':'){
            unsigned char empty[1] = {0};
            print_ndisasm_line(addr, empty, 0, tmp);
            continue;
        }
    
        char mn[64], rest[512]; split_mnemonic_rest(tmp, mn, rest);
        if(sec == SEC_DATA && is_data_directive_simple(mn)){
            int written = process_data_directive_simple(tmp, mn, rest, fo, addr);
            addr += (unsigned long)written;
            continue;
        }
        if(sec == SEC_BSS && is_bss_directive_simple(mn)){
            int written = process_bss_directive_simple(tmp, mn, rest, fo, addr);
            addr += (unsigned long)written;
            continue;
        }
        // instruction assembly
        unsigned char out[64]; int outn = 0;
        char op1[256], op2[256]; op1[0]=0; op2[0]=0;
        int parts = split_operands(rest, op1, op2);

        if(!strcmp(mn,"mov")){
            if(parts==2 && is_number_string(op2)){
                int rd = reg_index(op1);
                if(rd >= 0){
                    out[outn++] = (unsigned char)(0xB8 + rd);
                    outn += write_imm32(out+outn, (unsigned long)parse_number(op2));
                }
            } else if(parts==2 && !is_register(op2) && op2[0] != '['){
              //
                int rd = reg_index(op1);
                int lab = find_label(op2);
                unsigned long aval = 0;
                if(lab >= 0) aval = labels_addr[lab];
                out[outn++] = (unsigned char)(0xB8 + rd);
                outn += write_imm32(out+outn, aval);
            } else if(parts==2 && op2[0]=='['){
              
                
                char inner[256];
                strncpy(inner, op2+1, sizeof(inner)-1); inner[sizeof(inner)-1]=0;
                char *rb = strchr(inner,']'); if(rb) *rb=0;
                trim(inner);
                
                int is_sym = 1;
                for(int k=0; inner[k]; k++){
                    if(!(isalnum((unsigned char)inner[k]) || inner[k]=='_' || inner[k]=='.')) { is_sym = 0; break; }
                }
                if(is_sym && !is_register(inner)){
                    int rd = reg_index(op1);
                    int lab = find_label(inner);
                    unsigned long aval = 0;
                    if(lab >= 0) aval = labels_addr[lab];
                    // opcode 
                    out[outn++] = 0x8B; 
                    // encode modrm+sib+disp32 for absolute
                    outn += encode_abs_mem(out+outn, rd, aval);
                } else {
                    
                    
                    out[outn++] = 0x8B;
                    encode_sib_from_operand_and_modrm(op2, op1);
                    out[outn++] = generated_modrm;
                    if(generated_sib) out[outn++] = generated_sib;
                    for(int b=0;b<generated_disp_size;b++) out[outn++] = generated_disp[b];
                }
            } else if(parts==2){
             //reg+reg
                out[outn++] = 0x89;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++] = mod;
            }
        }
        else if(!strcmp(mn,"add")){
            if(parts==2){
                out[outn++]=0x01;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"sub")){
            if(parts==2){
                out[outn++]=0x29;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"xor")){
            if(parts==2){
                out[outn++]=0x31;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"cmp")){
            if(parts==2){
                out[outn++]=0x39;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"push")){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) out[outn++]= (unsigned char)(0x50 + r);
            }
        }
        else if(!strcmp(mn,"pop")){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) out[outn++]= (unsigned char)(0x58 + r);
            }
        }
        else if(!strcmp(mn,"inc")){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) out[outn++]= (unsigned char)(0x40 + r);
            }
        }
        else if(!strcmp(mn,"dec")){
            if(parts==1){
                int r = reg_index(op1);
                if(r>=0) out[outn++]= (unsigned char)(0x48 + r);
            }
        }
        else if(!strcmp(mn,"mul")){
            if(parts==2){
                out[outn++]=0x0F; out[outn++]=0xAF;
                unsigned char mod = modrm_encode_regreg(op2, op1);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"div")){
            if(parts==2){
                out[outn++]=0xF7;
                unsigned char mod = modrm_encode_regreg(op1, op2);
                out[outn++]=mod;
            }
        }
        else if(!strcmp(mn,"jmp")){
            if(parts==1){
                out[outn++]=0xE9;
                int lab = find_label(op1);
                long target = 0;
                if(lab>=0) target = (long)labels_addr[lab];
                long rel = target - (long)(addr + outn + 4);
                outn += write_imm32(out+outn, (unsigned long)rel);
            }
        }
        else if(!strcmp(mn,"int")){
            if(parts==1){
                out[outn++]=0xCD;
                out[outn++]=(unsigned char)(parse_number(op1) & 0xFF);
            }
        }

        if(outn > 0){
            write_and_print(fo, addr, out, outn, tmp);
            addr += (unsigned long)outn;
        } else {
       
            
            unsigned char empty[1] = {0};
            print_ndisasm_line(addr, empty, 0, tmp);
        }
    }
    fclose(fo);
    return 1;
}

// --- main ---

// new main 
/* ===================== MAIN ===================== */
int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: assembler <input.asm> <output.bin>\n");
        return 1;
    }

    const char *infile  = argv[1];
    const char *outfile = argv[2];

    /* ---- redirect stdout ---- */
    FILE *orig_stdout = stdout;
    FILE *log = fopen("terminal_output.txt", "w");
    if (!log) {
        perror("fopen terminal_output.txt");
        return 1;
    }
    stdout = log;

    /* ---- run assembler ---- */
    if (!pass1(infile)) {
        fprintf(stderr, "pass1 failed\n");
        return 1;
    }
    if (!pass2(outfile)) {
        fprintf(stderr, "pass2 failed\n");
        return 1;
    }

    printf("\nAssembling Done.\n");

    /* ---- restore stdout ---- */
    fflush(stdout);
    stdout = orig_stdout;
    fclose(log);

    return 0;
}




// old main for normal run in terminal
// int main(){
//     char infile[256], outfile[256];
//     printf("Enter input asm file: ");
//     if(scanf("%255s", infile) != 1) return 1;
//     printf("Enter output bin file: "); // 
//     if(scanf("%255s", outfile) != 1) return 1;

//     if(!pass1(infile)){ fprintf(stderr,"pass1 failed\n"); return 1; }
//     if(!pass2(outfile)){ fprintf(stderr,"pass2 failed\n"); return 1; }

//     printf("\nAssembling Done.\n");
//     return 0;
// }
