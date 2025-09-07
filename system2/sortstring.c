#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAXN 1000
#define MAXL 100

int sortbyfile(FILE* fp){
    char buffer[1024];
    int count=0;
    char* token;
    char name[MAXN][MAXL];
    while (fgets(buffer,sizeof(buffer),fp))
    {
        buffer[strcspn(buffer,"\n")]='\0';
        token =strtok(buffer, ",");
        while (token!=NULL)
        {
            strncpy(name[count],token,MAXL-1);
            name[count][MAXL - 1]='\0';
            count++;
            token=strtok(NULL,",");
        }
    }
   fclose(fp);
     //sorting
     for (int i = 0; i < count-1; i++){
        for (int j = i+1; j < count; j++)
        {
            if(strcmp(name[i],name[j])>0){
                char temp[MAXL];
                strcpy(temp,name[i]);
                strcpy(name[i],name[j]);
                strcpy(name[j],temp);
            }   
        }  
     } 

     fp=fopen("/home/matrix/Documents/vscode/system2/test.text","w");

     for (int i = 0; i < count; i++)
     {
        fprintf(fp,"%s",name[i]);
        if (i<count-1)
        {
            fprintf(fp,",");
            /* code */
        }
        
        /* code */
     }

return 0;
}

int sortbyarray(char name[MAXN][MAXL],int count){
    //int count=0;

    for (int i = 0; i < count-1; i++){
        for (int j = i+1; j < count; j++)
        {
            if(strcmp(name[i],name[j])>0){
                char temp[MAXL];
                strcpy(temp,name[i]);
                strcpy(name[i],name[j]);
                strcpy(name[j],temp);
            }   
        }  
     }


     for (int i = 0; i < count; i++)
     {
        printf("%s\n",name[i]);
     }
     
    return 0;
}

int main(){
    FILE *fp;
    fp=fopen("/home/matrix/Documents/vscode/system2/test.text","r");

    if (fp==NULL)
    {
        perror("File not find");
        exit(1);
    }
    printf("by file \n");
   // sortbyfile(fp);  //this sort by from file 
    printf("by array\n");
    char arr[][MAXL]={"rutik","prshant","karan"};
    int count=sizeof(arr)/sizeof(arr[0]);
    //printf("%d",count);
    sortbyarray(arr,count);

    return 0;
}