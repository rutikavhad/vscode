%{
#include<stdio.h>

%}

%%
if | else |{printf("%s is a keybord",yytext);}
[0-9]+ {printf("%s is a number",yytext);}
[a-zA-Z]+ {printf("%s is word",yytext);}

.|\n {ECHO;}

%%

int main(){
	
	printf("\n enter the string");


	yylex();
}

int yywrap(){

return 1;
}
