/* databss.c - simple data/bss handling in plain style */

#include "databss.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

static void trim(char *s){
    if(!s) return;
    while(*s && isspace((unsigned char)*s)) memmove(s, s+1, strlen(s));
    int n = strlen(s);
    while(n>0 && isspace((unsigned char)s[n-1])) s[--n]=0;
}

int is_data_directive_simple(const char *mn){
    if(!mn) return 0;
    return (!strcmp(mn,"db") || !strcmp(mn,"dw") || !strcmp(mn,"dd") || !strcmp(mn,"dq") || !strcmp(mn,"dt"));
}
int is_bss_directive_simple(const char *mn){
    if(!mn) return 0;
    return (!strcmp(mn,"resb") || !strcmp(mn,"resw") || !strcmp(mn,"resd") || !strcmp(mn,"resq") || !strcmp(mn,"rest"));
}

/* helper: parse comma-separated csv, keep quoted strings intact */
static int split_csv(char *buf, char **out, int maxout){
    int count=0;
    char *p = buf;
    while(*p && count < maxout){
        while(*p && isspace((unsigned char)*p)) p++;
        if(!*p) break;
        if(*p == '"' || *p == '\''){
            char q = *p++;
            out[count++] = p;
            while(*p && *p != q) p++;
            if(*p == q) { *p = 0; p++; }
            if(*p == ',') p++;
            continue;
        }
        out[count++] = p;
        while(*p && *p != ',') p++;
        if(*p == ','){ *p = 0; p++; }
    }
    return count;
}

static void print_ndisasm_line(unsigned long addr, const unsigned char *bytes, int n, const char *src){
    printf("%08lX  ", addr);
    for(int i=0;i<n;i++) printf("%02X", bytes[i]);
    if(n < 6){
        int pad = (6 - n) * 2;
        for(int i=0;i<pad;i++) putchar(' ');
    }
    printf("   %s\n", src);
}

long process_data_directive_size_simple(const char *mn, const char *args){
    if(!mn) return 0;
    if(!strcmp(mn,"db")){
        if(!args || !args[0]) return 0;
        char buf[1024]; strncpy(buf, args, sizeof(buf)-1); buf[sizeof(buf)-1]=0;
        char *tokens[256];
        int cnt = split_csv(buf, tokens, 256);
        long total = 0;
        for(int i=0;i<cnt;i++){
            if(tokens[i] && tokens[i][0]) total++;
        }
        return total;
    }
    if(!strcmp(mn,"dw")) return 2;
    if(!strcmp(mn,"dd")) return 4;
    if(!strcmp(mn,"dq")) return 8;
    if(!strcmp(mn,"dt")) return 10;
    if(!strcmp(mn,"resb")) return atol(args);
    if(!strcmp(mn,"resw")) return atol(args) * 2;
    if(!strcmp(mn,"resd")) return atol(args) * 4;
    if(!strcmp(mn,"resq")) return atol(args) * 8;
    if(!strcmp(mn,"rest")) return atol(args) * 10;
    return 0;
}

int process_data_directive_simple(const char *line, const char *mn, const char *args, FILE *fo, unsigned long address){
    unsigned char out[2048];
    int outn = 0;
    if(!mn) return 0;

    if(!strcmp(mn,"db")){
        char buf[1024]; strncpy(buf, args?args:"", sizeof(buf)-1); buf[sizeof(buf)-1]=0;
        char *tokens[256];
        int cnt = split_csv(buf, tokens, 256);
        for(int i=0;i<cnt;i++){
            if(!tokens[i]) continue;
            trim(tokens[i]);
            if(tokens[i][0] == '"' || tokens[i][0] == '\''){
                char *p = tokens[i];
                while(*p){ out[outn++] = (unsigned char)*p; p++; }
            } else {
                long v = strtol(tokens[i], NULL, 0);
                out[outn++] = (unsigned char)(v & 0xFF);
            }
        }
    } else if(!strcmp(mn,"dw")){
        long v = strtol(args, NULL, 0);
        out[outn++] = (unsigned char)(v & 0xFF);
        out[outn++] = (unsigned char)((v >> 8) & 0xFF);
    } else if(!strcmp(mn,"dd")){
        long v = strtol(args, NULL, 0);
        for(int k=0;k<4;k++) out[outn++] = (unsigned char)((v >> (8*k)) & 0xFF);
    } else if(!strcmp(mn,"dq")){
        unsigned long long v = strtoull(args?args:"0", NULL, 0);
        for(int k=0;k<8;k++) out[outn++] = (unsigned char)((v >> (8*k)) & 0xFF);
    } else if(!strcmp(mn,"dt")){
        for(int k=0;k<10;k++) out[outn++] = 0;
    }

    if(outn > 0) fwrite(out, 1, outn, fo);
    print_ndisasm_line(address, out, outn, line);
    return outn;
}

int process_bss_directive_simple(const char *line, const char *mn, const char *args, FILE *fo, unsigned long address){
    long cnt = atol(args);
    long bytes = 0;
    if(!strcmp(mn,"resb")) bytes = cnt;
    else if(!strcmp(mn,"resw")) bytes = cnt * 2;
    else if(!strcmp(mn,"resd")) bytes = cnt * 4;
    else if(!strcmp(mn,"resq")) bytes = cnt * 8;
    else if(!strcmp(mn,"rest")) bytes = cnt * 10;

    if(bytes <= 0){
        unsigned char empty[1] = {0};
        print_ndisasm_line(address, empty, 0, line);
        return 0;
    }

    unsigned char *z = (unsigned char*)calloc(1, (size_t)bytes);
    if(!z) return 0;
    fwrite(z,1,(size_t)bytes, fo);
    int printn = bytes > 16 ? 16 : (int)bytes;
    print_ndisasm_line(address, z, printn, line);
    free(z);
    return (int)bytes;
}
