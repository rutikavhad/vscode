#include<stdlib.h>
#include<stdio.h>
#include<string.h>

void main(){

    FILE *fp=fopen("/home/matrix/Documents/vscode/system2/file.text","r");
    if (fp==NULL)
    {
        perror("file not found");

        /* code */
    }
    //char myString[1000];
     //   fgets(myString,1000,fp);
        //printf("%s\n\n",myString);

        //this is main data for input file
        char name[50],class[10],course[50];
        int age,mobail;
        int target;
        printf("enter roll number ");
        scanf("%d",&target);
        //format of file
        //name age class    you can add  more if you want to add any thing
      fscanf(fp,"%s %s %s %s %s",name, name ,name,name,name);//use to ignore first line

        for (int i=1; i<=target;i++)
        {
            if(fscanf(fp,"%s %d %s %s %d",name,&age,class,course,&mobail)!=100){                            //Name Age Class Course Mobile
               // printf("%dthe name is %s\n",i,name);
            }
        }
        int ch;
        printf("Menu:\n1:Name\ttype 1\n2:age\ttype 2\n3:class\ttype 3\n4:course\ttype 4\n5:mobail\ttype 5\n");
        scanf("%d",&ch);
        switch (ch)
        {
        case 1:
            
        printf("roll no %d student name is %s",target,name);
            break;
         case 2:
            
        printf("roll no %d student age is %d",target,age);
            break;
            case 3:
            
        printf("roll no %d student class is %s",target,class);
            break;
            case 4:
            
        printf("roll no %d student cource is %s",target,course);
            break;
            case 5:
            
        printf("roll no %d student mobail is %d",target,mobail);
            break;
        default:
            break;
        }
                fclose(fp);
}