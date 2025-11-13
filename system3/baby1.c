#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

#define BUFLEN 1024

void happy_birthday_encrypt(char *msg) {
    for (int i = 0; msg[i]; i++)
        msg[i] = msg[i] ^ 0x2A;  // XOR each byte with 42
}

void happy_birthday_decrypt(char *msg) {
    happy_birthday_encrypt(msg); // XOR twice = original
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("Usage: %s <remote_ip> <remote_port> <local_port>\n", argv[0]);
        return 1;
    }

    char *remote_ip = argv[1];
    int remote_port = atoi(argv[2]);
    int local_port = atoi(argv[3]);

    int sock;
    char buf[BUFLEN];
    struct sockaddr_in local, remote;
    socklen_t len = sizeof(remote);

    sock = socket(AF_INET, SOCK_DGRAM, 0);

    local.sin_family = AF_INET;
    local.sin_port = htons(local_port);
    local.sin_addr.s_addr = INADDR_ANY;
    bind(sock, (struct sockaddr *)&local, sizeof(local));

    remote.sin_family = AF_INET;
    remote.sin_port = htons(remote_port);
    inet_pton(AF_INET, remote_ip, &remote.sin_addr);

    printf("Enter binary message: ");
    fgets(buf, BUFLEN, stdin);
    happy_birthday_encrypt(buf);

    sendto(sock, buf, strlen(buf), 0, (struct sockaddr *)&remote, sizeof(remote));
    printf("Encrypted message sent!\n");

    int n = recvfrom(sock, buf, BUFLEN, 0, (struct sockaddr *)&remote, &len);
    buf[n] = '\0';
    happy_birthday_decrypt(buf);
    printf("Received decrypted reply: %s\n", buf);

    close(sock);
    return 0;
}
