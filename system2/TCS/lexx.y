%{
#include <stdio.h>
int yylex(void);
void yyerror(char *s);
%}

%token END ONE ZERO ANOTHER
%start st

%%
st: A END       { printf("Accepted\n"); }
 ;

A: A ZERO
 | A ONE
 |
 ;
%%

void yyerror(char *s)
{
    fprintf(stderr, "Error: %s\n", s);
}

int main(void)
{
    printf("Enter a sequence of 0s and 1s, then press Enter:\n");
    yyparse();
    return 0;
}
