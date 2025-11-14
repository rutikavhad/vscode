//this file want to run 
//urecv.c file
//baby0.c self
//usend.c file
//file req = config.txt
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <errno.h>

#define BUFLEN 1024

int main(int argc, char *argv[])
{
    char remote_ip[64] = "127.0.0.1";
    int ear_port = 0, mouth_port = 0;
    int ear_size = BUFLEN, mouth_size = BUFLEN, self_size = 1;

    const char *config_file = "config.txt";
    if (argc > 1)
        config_file = argv[1];

    FILE *f = fopen(config_file, "r");
    if (!f)
    {
        perror("config file not found");
        exit(1);
    }

    char line[128];
    while (fgets(line, sizeof(line), f))//this read ear,mouth,remote_ip,self_size port  from file
    {
        if (sscanf(line, "EAR_PORT=%d", &ear_port) == 1)  
            continue;
        if (sscanf(line, "MOUTH_PORT=%d", &mouth_port) == 1) 
            continue;
        if (sscanf(line, "REMOTE_IP=%63s", remote_ip) == 1)
            continue;
        if (sscanf(line, "SELF_SIZE=%d", &self_size) == 1)
            continue;
    }
    fclose(f);

    printf("Config:\n");
    printf(" EAR_PORT=%d\n MOUTH_PORT=%d\n REMOTE_IP=%s\n SELF_SIZE=%d\n\n", ear_port, mouth_port, remote_ip, self_size); // show a which poer ip used to send recive

    int s1, s2, n, len;
    char buf[BUFLEN];
    struct sockaddr_in ear, mouth, remote;

    s1 = socket(AF_INET, SOCK_DGRAM, 0); //for recive
    s2 = socket(AF_INET, SOCK_DGRAM, 0); // for send

    int opt = 1;
    setsockopt(s1, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)); //use for avoid port allrady used

    ear.sin_family = AF_INET;
    ear.sin_port = htons(ear_port);
    ear.sin_addr.s_addr = INADDR_ANY;

    if (bind(s1, (struct sockaddr *)&ear, sizeof(ear)) < 0)
    {
        fprintf(stderr, "Bind failed on port %d: %s\n", ear_port, strerror(errno));
        exit(1);
    }

    remote.sin_family = AF_INET;
    remote.sin_port = htons(mouth_port);
    if (inet_pton(AF_INET, remote_ip, &remote.sin_addr) <= 0)
    {
        fprintf(stderr, "Invalid IP: %s\n", remote_ip);
        exit(1);
    }

    printf("baby0%d waiting on port %d ...\n", self_size, ear_port);
    len = sizeof(mouth);

    n = recvfrom(s1, buf, BUFLEN - 1, 0, (struct sockaddr *)&mouth, &len);
    if (n < 0)
    {
        perror("recv_from failed");
        exit(1);
    }
    buf[n] = '\0';

    printf("baby%d got: %s\n", self_size, buf);

    char msg[BUFLEN];
    snprintf(msg, sizeof(msg), "[baby%d ACK] %s", self_size, buf);

    if (sendto(s2, msg, strlen(msg), 0, (struct sockaddr *)&remote, sizeof(remote)) < 0)
        perror("send_to failed");
    else
        printf("baby0%d sent to %s:%d\n", self_size, remote_ip, mouth_port);///send to mouth

    close(s1);
    close(s2);
    return 0;
}
