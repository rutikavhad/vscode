#include <stdio.h>

int main() {

    int a, b, c, d, e;

    a = 5;          
    b = 10;         

    // IF-ELSE
    if (a > 0) {
        c = a + b;  
        a = c + 1; 
    } else {
        b = a + 2;  
    }

    d = a + b;      

    // WHILE LOOP
    while (d < 50) {
        a = d + b;  
        d = a + 1;  
    }

    // AFTER LOOP
    e = a + d;      
    c = e + b;      

    return 0;
}