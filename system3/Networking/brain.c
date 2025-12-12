#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFLEN 1024  //massage size

int main()
{
  int s1, s2, n, len;
  char buf[BUFLEN];
  struct sockaddr_in brain, mouth, ear;

  // socket s1 for receiving from mouth
  s1 = socket(AF_INET, SOCK_DGRAM, 0);

  // socket s2 for sending to ear
  s2 = socket(AF_INET, SOCK_DGRAM, 0);

  // brain listens on port 4321
  brain.sin_family = AF_INET;
  brain.sin_port = htons(6000);
  brain.sin_addr.s_addr = INADDR_ANY;

  // bind s1 to port 4321 so brain can receive messages from mouth
  bind(s1, (struct sockaddr *)&brain, sizeof(brain));

  // ear address → where brain will send reply
  ear.sin_family = AF_INET;
  ear.sin_port = htons(5000);
  ear.sin_addr.s_addr = INADDR_ANY;

  len = sizeof(mouth);  // recvfrom writes sender address (mouth) here

  printf("brain waiting for mouth...\n");

  // receive message from mouth
  n = recvfrom(s1, buf, BUFLEN, 0, (struct sockaddr *)&mouth, &len);
  buf[n] = '\0';  // null-terminate message
  printf("brain got: %s\n", buf);

  // add brain message to end of received text
  strcat(buf, "this is a brain");

  // send modified message to ear (port 1234)
  sendto(s2, buf, strlen(buf), 0, (struct sockaddr *)&ear, sizeof(ear));
  printf("brain sent to ear\n");

  return 0;
}
