#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <errno.h>

int main(int argc, char *argv[])
{
    int buflen = 1024; //
    char remote_ip[64] = "127.0.0.1"; 
    int ear_port = 0, mouth_port = 0;
    int ear_size = buflen, mouth_size = buflen, self_size = 1;

    const char *config_file = "params.config"; //read file
    if (argc > 1)
        config_file = argv[1];

    FILE *f = fopen(config_file, "r"); //read data from file
    if (!f)
    {
        perror("params file not found");
        exit(1);
    }

    char line[128];
    while (fgets(line, sizeof(line), f))
    {
        if (sscanf(line, "EAR_PORT=%d", &ear_port) == 1) // read ear port form file
            continue;
        if (sscanf(line, "MOUTH_PORT=%d", &mouth_port) == 1)  //read mouth port form file
            continue;
        if (sscanf(line, "REMOTE_IP=%63s", remote_ip) == 1)  // read loaclhost ip from file
            continue;
        if (sscanf(line, "SELF_SIZE=%d", &self_size) == 1)  //self data read size
            continue;
        if (sscanf(line, "BUFLEN=%d", &buflen) == 1) //this used for mouth and ear size (massage size)
            continue;

    }
    fclose(f);

    printf("Config:\n");
    printf(" EAR_PORT=%d\n MOUTH_PORT=%d\n REMOTE_IP=%s\n SELF_SYSTEM_SIZE=%d\n EAR&MOUTH_SIZE=%d\n\n",
           ear_port, mouth_port, remote_ip, self_size,buflen);

    int s1, s2, n, len;
    char buf[buflen];
    struct sockaddr_in ear, mouth, remote;

    s1 = socket(AF_INET, SOCK_DGRAM, 0);
    s2 = socket(AF_INET, SOCK_DGRAM, 0);

    int opt = 1;
    setsockopt(s1, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    ear.sin_family = AF_INET;  // ipv4
    ear.sin_port = htons(ear_port); // set port
    ear.sin_addr.s_addr = INADDR_ANY; // set address 

    if (bind(s1, (struct sockaddr *)&ear, sizeof(ear)) < 0) //bind socket to ear for recive data 
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

    printf("baby%d waiting on port %d ...\n", self_size, ear_port);
    len = sizeof(mouth);

    n = recvfrom(s1, buf, buflen - 1, 0, (struct sockaddr *)&mouth, &len); // reading data(massage) from ear
    if (n < 0)
    {
        perror("recvfrom failed");
        exit(1);
    }
    buf[n] = '\0';

    printf("baby%d got: %s\n", self_size, buf);

    char msg[buflen];
    snprintf(msg, sizeof(msg), "[baby%d ACK] %s", self_size, buf);  // sent this data (massage) to mouth

    if (sendto(s2, msg, strlen(msg), 0, (struct sockaddr *)&remote, sizeof(remote)) < 0)
        perror("sendto failed");
    else
        printf("baby%d sent to %s:%d\n", self_size, remote_ip, mouth_port);

    close(s1); // close ear port
    close(s2); // close mouth port
    return 0;
}
