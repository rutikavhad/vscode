%{
#include<stdio.h>
%}

%%

 

#[0-9]+ {printf("only digit");}
#[a-z]+ {printf("only small a-z");}
[A-B]+ {printf("capital ABC");}


.Q*R  {printf("start Q end R");}

.*pqr.* {printf("substring is pqr");}

.*abc {printf("end with abc\n");}

abc.* {printf("strt with abc\n");}

[0-9]{3} {printf("limit num");}
#[0-9]{2,} {printf("only list n digit ");}
#[0-9]{2,4} {printf("form 2 to 4 digit only");}
g{1} {printf("get single g only");}

%%

int main(){
printf("enter string\n");
yylex();
}
int yywrap(){
return 0;
}







