// we want a file contain: mov eax, [ebx + esi*4]
// this type of input: .. .., [base + index*scale]


// we want a output like a  : SIB byte (binary): 10010011
// SIB byte (hex): 0x93

// scall factors: {1 , 2, 4, 8}
// general-purpose register
// :  eax=000, ecx=001, edx=010, ebx=011, esp=100, ebp=101, esi=110, edi=111

//code

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

int array[8];
/*THIS IS MAKE BINARY TO HEXA DECIMAL NUMBER*/
int binary(){
   //binary to hexa
    int size=7;
	unsigned int number=0;
    int number1=0;
	unsigned int binary=2;
	unsigned int i=0;
	unsigned int dd=size-1;
	if(array[7]==1){
	
		number=1;
	}
	i=0;
	while(i<3){
		//printf("%d\n",array[dd]);
		if(array[dd]==1){	
            number=number+binary;	
		}
			binary=binary*2;
		dd--;
		i++;
	}//
	//printf("\nthe Whole  number is : %d\n",number);
//this for 2nd part
    if(array[3]==1){	
	number1=1;
	}
	i=0;
    binary=2;
    dd=dd-1;
	while(i<3){
		//printf("%d\n",array[dd]);
		if(array[dd]==1){	
            number1=number1+binary;	
		}
			binary=binary*2;
		dd--;
		i++;
	}

//output binary is
printf("\nDecimal Number is= 0x%d\t0x%d\n",number1,number);
    //make hexa

    int value=0,value1=0;
    //0to3
    for (int i = 0; i < 4; i++) {
        value = (value << 1) | array[i]; 
    }
    //4to7
     for (int i = 4; i < 8; i++) {
        value1 = (value1 << 1) | array[i]; 
    }
//hexa ouput
     printf("Hex=0x%02X\t0x%02X\n", value,value1);
    

return 0;  
}

/*                  THIS FOR GET REGISTER BINARY NUMBER BY MENUALY                    */
int regg(char reg[4],int flag){
    printf("\n %s",reg);
    //eax=000;
    if (strcmp(reg, "eax") == 0 )
    {

    if (flag==0)
    {
        array[0]=0;
        array[1]=0;
        array[2]=0;
        flag=1;
    }
    else{
       
        array[3]=0;
        array[4]=0;
        array[5]=0;
    }
        
    }
    //ecx==001
    else if (strcmp(reg, "ecx") == 0 )
    {

    if (flag==0)
    {
        array[0]=0;
        array[1]=0;
        array[2]=1;
        flag=1;
    }
    else{
       
        array[3]=0;
        array[4]=0;
        array[5]=1;
    }
        
    }
    //edx==010
    else if (strcmp(reg, "edx") == 0 )
    {

    if (flag==0)
    {
        array[0]=0;
        array[1]=1;
        array[2]=0;
        flag=1;
    }
    else{
       
        array[3]=0;
        array[4]=1;
        array[5]=0;
    }
        
    }
    //ebx==011
    else if (strcmp(reg, "ebx") == 0 )
    {

    if (flag==0)
    {
        array[0]=0;
        array[1]=1;
        array[2]=1;
        flag=1;
    }
    else{
       
        array[3]=0;
        array[4]=1;
        array[5]=1;
    }
        
    }
    //esp==100
    else if (strcmp(reg, "esp") == 0 )
    {

    if (flag==0)
    {
        array[0]=1;
        array[1]=0;
        array[2]=0;
        flag=1;
    }
    else{
       
        array[3]=1;
        array[4]=0;
        array[5]=0;
    }
        
    }
    //ebp==101
    else if (strcmp(reg, "ebp") == 0 )
    {

    if (flag==0)
    {
        array[0]=1;
        array[1]=0;
        array[2]=1;
        flag=1;
    }
    else{
       
        array[3]=1;
        array[4]=0;
        array[5]=1;
    }
        
    }
    //esi==110
    else if (strcmp(reg, "esi") == 0 )
    {

    if (flag==0)
    {
        array[0]=1;
        array[1]=1;
        array[2]=0;
        flag=1;
    }
    else{
       
        array[3]=1;
        array[4]=1;
        array[5]=0;
    }
        
    }
    //edi=111
    else if (strcmp(reg, "edi") == 0 )
    {

    if (flag==0)
    {
        array[0]=1;
        array[1]=1;
        array[2]=1;
        flag=1;
    }
    else{
       
        array[3]=1;
        array[4]=1;
        array[5]=1;
    }
        
    }
   return 0;
}
/*             THIS FOR GET BASE NUMBER BINARY                */
int basse(int num){
    switch (num) {
        case 1: return 0;
        case 2: return 1;  
        case 4: return 2;  
        case 8: return 3;
        default: return -1;   
    }
}


int main(){

    //get input file
    char filepath[256];
     FILE *fp;

     printf("Enter .asm File Path");
     scanf("%255s",filepath);

     fp=fopen(filepath,"r");
  // fp=fopen("/home/matrix/Documents/vscode/system2/strcpy.asm","r");
    if (fp==NULL)
    {
        perror("file not found");
        exit(1);
    }

    char buffer[256];
    int linenumber =0;
    char *start, *end;
    char operand[128];
    char * token;
    char reg[4];
    char reg11[4]="",reg22[4]="";
    int base=1;
    int regCount=0;
    /**********************************************************************READ ONLY REGISTER [.....]**************************************************************************************** */
while (fgets(buffer, sizeof(buffer), fp)) {
    linenumber++;

    start = strchr(buffer, '[');
    end   = strchr(buffer, ']');

    if (start && end) {
        // reset for each line
        reg11[0] = reg22[0] = '\0';
        base = 1;
        regCount = 0;

        strncpy(operand, start + 1, end - start - 1);
        operand[end - start - 1] = '\0';  // null terminate

        // tokenize
        token = strtok(operand, " +*");
        while (token != NULL) {
            if (strlen(token) == 3 && isalpha(token[0])) {
                if (regCount == 0) strcpy(reg11, token);
                else strcpy(reg22, token);
                regCount++;
            } else if (isdigit(token[0])) {
                base = atoi(token);  // convert string to int
            }
            token = strtok(NULL, " +*");
        }

        printf("Line %d: reg1 = %s, reg2 = %s, base = %d\n",
               linenumber, reg11, reg22, base);

        // === MOVE THE REG/BASSE/BINARY PROCESSING HERE ===
        int flag=0;
        strcpy(reg, reg11);
        regg(reg,flag);
        flag=1;
        strcpy(reg, reg22);
        regg(reg,flag);

        int bass=basse(base);
        array[6] = bass & 1;     //lsb
        array[7] = (bass >> 1) & 1; //msb

        binary();

        // Print binary for testing
        int w=0;
        printf("Binary number is =");
        while (w<8){
            printf("%d",array[w]);
            w++;
        }
        printf("\n\n");
    }
}
}