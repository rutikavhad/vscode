#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SIZE 1024 // this is  a  1 chunk can send data
#define END "END" // mark as massage end after type massage and hit enter

void xor_crypt(char *d, int n) { // this will used for simepl Encrypt & decrypt
    for (int i = 0; i < n; i++)
        d[i] ^= 0x2A; // send only binary data
}

int main(int c, char *v[]) {
    if (c != 3) {
        printf("use: %s <remote_port> <local_port>\n", v[0]); // used to get sender and recever port address
        return 1;
    }

    int rport = atoi(v[1]), lport = atoi(v[2]);
    int s = socket(AF_INET, SOCK_DGRAM, 0); // this socket connection used  ipv4 and udp 
    if (s < 0) { perror("socket"); return 1; } 

    struct sockaddr_in me = {0}, you = {0};  // used for bind local port
    me.sin_family = AF_INET;                 // used ipv4 socket connection
    me.sin_port = htons(lport);
    me.sin_addr.s_addr = INADDR_ANY; 
    if (bind(s, (void *)&me, sizeof(me)) < 0) {
        perror("bind"); return 1;
    }
    //this is a remote setup
    you.sin_family = AF_INET;
    you.sin_port = htons(rport);
    inet_pton(AF_INET, "127.0.0.1", &you.sin_addr);  // used  a localhost ip for local system
    // ask    sender or reciver
    char mode[10];
    printf("mode (send/recv): ");
    fgets(mode, sizeof(mode), stdin);
    mode[strcspn(mode, "\n")] = 0;

    char buf[SIZE], all[65536] = {0}; // set max massage size 65 kb only as udp can send at one time not more then this
    socklen_t len = sizeof(you);

    // === SEND ===
    if (!strcmp(mode, "send")) {
        printf("enter message:\n");
        fgets(all, sizeof(all), stdin);
        int total = strlen(all), sent = 0; //this will read massage upto 65kb 
        // this used to make chunk of massage size 1024
        //if use max or large then 9 kb a packet may be lost, udp can't handle it .
        while (sent < total) {
            int chunk = (total - sent > SIZE) ? SIZE : (total - sent);
            memcpy(buf, all + sent, chunk);
            xor_crypt(buf, chunk); //  this will  used to Encrypt massage 
            sendto(s, buf, chunk, 0, (void *)&you, len);
            sent += chunk;
            printf("sent %d/%d\n", sent, total);
            usleep(3000); // this used for avoid packet lost
        }
        strcpy(buf, END);
        xor_crypt(buf, strlen(END));
        sendto(s, buf, strlen(END), 0, (void *)&you, len);
        printf("done.\n");
    }

    // === RECEIVE === 
    else if (!strcmp(mode, "recv")) {
        printf("listening on %d...\n", lport);
        int pos = 0, n;
        while (1) {
            n = recvfrom(s, buf, SIZE, 0, (void *)&you, &len);
            xor_crypt(buf, n); // this will used to decrypt massage 
            buf[n] = 0;
            if (!strcmp(buf, END)) break;
            memcpy(all + pos, buf, n);
            pos += n;
            printf("got %d bytes\n", n);
        }
        all[pos] = 0;
        printf("\nfull msg (%d bytes):\n%s\n", pos, all); // this will print all massage
    }

    else printf("bad mode\n"); // if got error data

    close(s); // close connections
    return 0;
}
