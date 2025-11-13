// brain.c - receive from mouth (4321), send to ear (1234)

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFLEN 1024

int main()
{
  int s1, s2, n, len;
  char buf[BUFLEN];
  struct sockaddr_in brain, mouth, ear;

  s1 = socket(AF_INET, SOCK_DGRAM, 0);
  s2 = socket(AF_INET, SOCK_DGRAM, 0);

  brain.sin_family = AF_INET;
  brain.sin_port = htons(4321);
  brain.sin_addr.s_addr = INADDR_ANY;

  bind(s1, (struct sockaddr *)&brain, sizeof(brain));

  ear.sin_family = AF_INET;
  ear.sin_port = htons(1234);
  ear.sin_addr.s_addr = INADDR_ANY;

  len = sizeof(mouth);
  printf("brain waiting for mouth...\n");
  n = recvfrom(s1, buf, BUFLEN, 0, (struct sockaddr *)&mouth, &len); // recv from mouth
  buf[n] = '\0';
  printf("brain got: %s\n", buf);

  strcat(buf, "this is a brain");
  sendto(s2, buf, strlen(buf), 0, (struct sockaddr *)&ear, sizeof(ear)); // send to ear
  printf("brain sent to ear\n");

  return 0;
}

