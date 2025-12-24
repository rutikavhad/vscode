#ifndef DATABSS_H
#define DATABSS_H

#include <stdio.h>

/* simple helpers used by main.c */

/* Determine if mnemonic is a data directive (db/dw/dd/dq/dt) */
int is_data_directive_simple(const char *mn);

/* Determine if mnemonic is a bss directive (resb/resw/resd/resq/rest) */
int is_bss_directive_simple(const char *mn);

/* In pass1 we need to estimate how many bytes data directives allocate */
long process_data_directive_size_simple(const char *mn, const char *args);

/* In pass2 we write bytes and print; returns bytes written */
int process_data_directive_simple(const char *line, const char *mn, const char *args, FILE *fo, unsigned long address);

/* process bss: write zeros and print; returns bytes written */
int process_bss_directive_simple(const char *line, const char *mn, const char *args, FILE *fo, unsigned long address);

#endif
