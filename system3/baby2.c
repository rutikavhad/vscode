#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BROADCAST_PORT 6000
#define MSG "I_AM_ONLINE"
#define BUFLEN 1024

int main() {
    int sock;
    struct sockaddr_in broadcast_addr, recv_addr;
    socklen_t addrlen = sizeof(recv_addr);
    char buf[BUFLEN];

    sock = socket(AF_INET, SOCK_DGRAM, 0);

    int broadcastEnable = 1;
    setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcastEnable, sizeof(broadcastEnable));

    broadcast_addr.sin_family = AF_INET;
    broadcast_addr.sin_port = htons(BROADCAST_PORT);
    broadcast_addr.sin_addr.s_addr = inet_addr("255.255.255.255");

    if (fork() == 0) {
        // child keeps sending broadcast
        while (1) {
            sendto(sock, MSG, strlen(MSG), 0, (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
            sleep(2);
        }
    } else {
        // parent listens for others
        struct sockaddr_in local;
        local.sin_family = AF_INET;
        local.sin_port = htons(BROADCAST_PORT);
        local.sin_addr.s_addr = INADDR_ANY;
        bind(sock, (struct sockaddr *)&local, sizeof(local));

        while (1) {
            int n = recvfrom(sock, buf, BUFLEN, 0, (struct sockaddr *)&recv_addr, &addrlen);
            buf[n] = '\0';
            printf("System %s is online\n", inet_ntoa(recv_addr.sin_addr));
        }
    }
}
