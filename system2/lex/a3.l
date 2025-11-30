%{
#include <stdio.h>

int a = 0;
int b = 0;
%}

%%
a        { a++; }
b        { b++; }

%%

int main()
{
    yylex();    /* run lexer */

    if (a == b)
        printf("a and b are equal\n");
    else
        printf("a and b are NOT equal\n");

    return 0;
}

int yywrap() { return 1; }
