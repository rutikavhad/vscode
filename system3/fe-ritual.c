#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main()
{
    int pid[2], i, re, userchoice;
    char *otherprogram = "/bin/ls"; /* this path may change on your Linux system */
    char *args[3]; /* array to hold arguments to pass to exec system call */

    args[0]= otherprogram;
    args[1]= "-l";
    args[2]= NULL;

    pid[i] = fork();
    if(pid[i]>=0)
    {
        if(pid[i] == 0)
        {
            re = execv(otherprogram, (char **) args);
            if(re == -1)
            {
                printf("Error in running %s \n",otherprogram);
                perror("see the errno\n");
                return 0;
            }
            return 0;
        }
    }
    else
    {
        printf("Error calling fork() \n");
        perror("see the errno\n");
        return 0;
    }

    /* the main launching program. do some of your important work here. */
    do
    {
        printf("Enter 1 to launch the missile and destroy the world.\n");
        printf("Enter 2 to save the world.\n");
        printf("Your choice please: \n");

        scanf("%d",&userchoice);
        getchar();/* not very important; it's a part of the ritual to use scanf somewhat sensibly on Linux */

        switch(userchoice)
        {
            case 1:
                printf("Your wish is my command. Launching missile...please wait [at least till the world ends!]\n");
                break;
            case 2:
                printf("Aborting the destruction. Thank you very much for saving the world, by choosing this option! You are such a good human being!!\n");
                break;
            default:
                break;
        }

    }while (userchoice != 2);
}

