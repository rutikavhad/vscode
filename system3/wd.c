#include <stdlib.h>
#include <stdio.h>

int main()
{
  int i;
  int nums[] = {3432,322,-43,0,5};
  char umsg[1024]="gud morning";
  FILE* fp;
  if ((fp = fopen("data", "wb")) == NULL)
  {
     printf("some error while opening file for writing data.\n");
     exit(1);
  }

  /* let's write some numbers to the output file */
  for (i=0;i<5;++i)
      fwrite(&nums[i], sizeof(int), 1, fp);
  fflush(fp);
  /* now let's write some ASCII text to the output file
   * note that this text shall be written after the
   * numbers in the output file 
   * */
  fwrite(umsg, 11, 1, fp);
  /* fflush need not be used this much frequently
   * here it is used to just emphasize its usage */
  fflush(fp);
  printf("data written to the file named \"data\"\n");
  fclose(fp);
  return 0;
}

