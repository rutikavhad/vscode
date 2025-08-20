#include<stdio.h>
#include<string.h>


enum Registers{
    eax = 0b000,
    ecx = 0b001,
    edx = 0b010,
    ebx = 0b011,
    esp = 0b100,
    ebp = 0b101,
    esi = 0b110,
    edi = 0b111
};

int getRegisterCode(const char *reg)
{
    if(strcmp(reg,"eax")==0) return eax;
    if(strcmp(reg,"ecx")==0) return ecx;
    if(strcmp(reg,"edx")==0) return edx;
    if(strcmp(reg,"ebx")==0) return ebx;
    if(strcmp(reg,"esp")==0) return esp;
    if(strcmp(reg,"ebp")==0) return ebp;
    if(strcmp(reg,"esi")==0) return esi;
    if(strcmp(reg,"edi")==0) return edi;
    return -1;
}

int main()  
{
    FILE *fp;
    char ch[256] ;
    
    
    // Opening the .asm file and reading the content from the file that start from main:

    fp = fopen("mod_rm.asm","r");
    if(fp==NULL)
    {
        printf("Error opening  file\n");
        return 1;
    }

   
    // if the line containing any blankspace or comment(;;) , the line get ignore or skip 


    while(fgets(ch,sizeof(ch),fp))
    {
        if(ch[0] == '\n' || ch[0] ==';')
        continue;  
        

        char *token = strtok(ch,  " ,\t\n");
        if(token==NULL)
        continue;   

        if(strcmp(token,"mov") == 0 ||
          strcmp(token,"xor") == 0 ||
          strcmp(token,"add") == 0 || 
          strcmp(token,"sub") == 0 ||
          strcmp(token,"cmp") == 0) 
        {
                char *arg1 = strtok(NULL,  " ,\t\n");
                char *arg2 = strtok(NULL,  " ,\t\n");


                if(arg1 && arg2)
                {
                    int dest = getRegisterCode(arg1);
                    int src = getRegisterCode(arg2);

                    if(dest != -1 && src != -1)
                    {
                        int reg = src;
                        int rm = dest;

                        int modrm = (0b11 << 6) | (reg << 3) | rm;
                        printf("0x%X\n", modrm);                    
                    }
                }
        }
    
       
    }

    fclose(fp);
    return 0;
}

 
