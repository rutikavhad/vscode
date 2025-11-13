%{
#include <stdio.h>
#include "y.tab.h" 
%}

%%
1           { return ONE; }
0           { return ZERO; }
\n          { return END; }
[ \t]+      { /* ignore whitespace */ }
.           { return ANOTHER; }
%%

int yywrap(void) {
    return 1;
}
