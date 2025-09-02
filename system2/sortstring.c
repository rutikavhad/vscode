#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int sort(){

}


int main(){
    FILE *fp;
    fp=fopen("/home/matrix/Documents/vscode/system2/test.text","r");

    if (fp==NULL)
    {
        perror("File not find");
        exit(1);
    }
    
    
    char name[50];
    

    fscanf(fp,"%s\n",name);

    printf("%s",name);
    fclose(fp);
    return 0;
}