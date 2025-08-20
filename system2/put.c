#include <stdio.h>
#include <string.h>



#include <stdio.h>

int arrays() {
    int a[8] = {1,1,1,1,1,0,1,1}; // example bits (SIB = 10010011)
    int value = 0;

    // combine bits into an integer
    for (int i = 4; i < 8; i++) {
        value = (value << 1) | a[i];  // shift left, add current bit
    }

    // print in binary and hex
    printf("Decimal = %d\n", value);
    printf("Hex     = 0x%02X\n", value);

    return 0;
}


int simple() {
    int num = 01;
    int a[10];   // array to store digits
    int i = 6;

    // extract digits from right to left
   while (num > 0) {
        a[i] = num % 10;  // take last digit
        num /= 10;        // remove last digit
        i++;
    }

 for (int j = 0; j < i; j++) {
        printf("a[%d] = %d\n", j, a[j]);
    }


    return 0;
}


int numtoarray() {
    int num = 100;
    int a[10];  
    char str[20];
    int stindex = 6;

    sprintf(str, "%d", num);

    for (int i = 0; i < strlen(str); i++) {
        a[stindex + i] = str[i] - '0';  
    }
    int i=0;
    while (i<=10)
    {
        printf("%c\t",str[i]);
        i++;
       
    }
    
    return 0;
}
int arr[3];
int numm(int num){
    switch (num) {
        case 1: return 00;
        case 2: return 01;  
        case 4: return 10;  
        case 8: return 11;
        default: return -1;   
    }
}



int main(){
    //numtoarray();
    int num=4;
    //printf("%d",numm(num));
    //simple();
    arrays();


    return 0;
}
