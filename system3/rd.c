#include <stdlib.h>
#include <stdio.h>

int main()
{
  int i,data;
  char umsg[1024]="this string will be changed.\n";
  FILE* fp;
  if ((fp = fopen("data", "rb")) == NULL)
  {
    printf("some error while opening file for reading data.\n");
    exit(1);
  }
  /* let's read the numbers from the input file */
  for (i=0;i<5;++i)
  {
    fread(&data, sizeof(int), 1, fp);
    printf("nums[%d]: %d\n",i, data);
  }
  /* now let's read the text from the input file 
   * note that this text follows the numbers in the input file
   * */
  fread(&umsg, 11, 1, fp);
  printf("user message received is: %s",umsg);
  fclose(fp);
  return 0;
}

