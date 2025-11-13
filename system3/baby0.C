#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFLEN 1024

int main() {
    FILE *f = fopen("params.txt", "r");
    if (!f) {
        perror("params.txt not found");
        exit(1);
    }

    int ear_port = 0, mouth_port = 0;
    char remote_ip[64];
    char line[128];

    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, "EAR_PORT=%d", &ear_port)) continue;
        if (sscanf(line, "MOUTH_PORT=%d", &mouth_port)) continue;
        if (sscanf(line, "REMOTE_IP=%s", remote_ip)) continue;
    }
    fclose(f);

    int s1, s2, n;
    socklen_t len;
    char buf[BUFLEN];
    struct sockaddr_in ear, mouth, remote;

    s1 = socket(AF_INET, SOCK_DGRAM, 0);
    s2 = socket(AF_INET, SOCK_DGRAM, 0);

    ear.sin_family = AF_INET;
    ear.sin_port = htons(ear_port);
    ear.sin_addr.s_addr = INADDR_ANY;
    bind(s1, (struct sockaddr *)&ear, sizeof(ear));

    remote.sin_family = AF_INET;
    remote.sin_port = htons(mouth_port);
    inet_pton(AF_INET, remote_ip, &remote.sin_addr);

    printf("Waiting for message...\n");
    len = sizeof(mouth);
    n = recvfrom(s1, buf, BUFLEN, 0, (struct sockaddr *)&mouth, &len);
    buf[n] = '\0';
    printf("Received: %s\n", buf);

    strcat(buf, " | Reply from system");
    sendto(s2, buf, strlen(buf), 0, (struct sockaddr *)&remote, sizeof(remote));
    printf("Replied to %s:%d\n", remote_ip, mouth_port);

    close(s1);
    close(s2);
    return 0;
}
