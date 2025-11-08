%{
#include <stdio.h>
%}

%option noyywrap

%%
(000.*111)|(111.*000)      { printf("contain both 000 and 111\n"); }
000|111                    { printf("contain 000 or 111\n"); }
^0.*1$                     { printf("start 0 end 1\n"); }
^[0-9]*[02468]$            { printf("even\n"); }
^[^a]*a([^a]*a){0,2}[^a]*$ { printf("at least one 'a' but no more than 3\n"); }
_?[0-9]+                   { printf("int number\n"); }
\n                         { /* ignore blank lines */ }
.                          { printf("no match: %s\n", yytext); }
%%

int main(void) {
    printf("Enter input (Ctrl+D to end):\n");
    yylex();
    return 0;
}
