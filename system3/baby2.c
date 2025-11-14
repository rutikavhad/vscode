#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define GROUP "239.0.0.1" //multicast group
#define PORT 6000 //single udp port  for all systems

int main() {
    int s, yes=1, n;
    struct sockaddr_in me, g, r;
    socklen_t rl = sizeof(r);
    char buf[128], seen[128][128];
    int sc = 0;
    //create udp socket
    s = socket(AF_INET, SOCK_DGRAM, 0);

    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));//multisystem can connect same port 
#ifdef SO_REUSEPORT
    setsockopt(s, SOL_SOCKET, SO_REUSEPORT, &yes, sizeof(yes));
#endif
    setsockopt(s, IPPROTO_IP, IP_MULTICAST_LOOP, &yes, sizeof(yes));// multicast packet in loop
    //bind port for receive "system online"
    me.sin_family = AF_INET;
    me.sin_port = htons(PORT);
    me.sin_addr.s_addr = INADDR_ANY;
    bind(s, (void *)&me, sizeof(me));

    struct ip_mreq m; 
    m.imr_multiaddr.s_addr = inet_addr(GROUP);
    m.imr_interface.s_addr = INADDR_ANY;
    setsockopt(s, IPPROTO_IP, IP_ADD_MEMBERSHIP, &m, sizeof(m));
    // this used for sand for multicast
    g.sin_family = AF_INET;
    g.sin_port = htons(PORT);
    g.sin_addr.s_addr = inet_addr(GROUP);

    char id[64]; //this for get unique id for each system
    snprintf(id, sizeof(id), "PID_%d", getpid());

    if (fork() == 0) { //fork used for send & recieve
        
        sleep(1);
        sendto(s, id, strlen(id), 0, (void *)&g, sizeof(g)); // this sender as child
        
        return 0;
    } else {
        for (;;) {
            n = recvfrom(s, buf, 127, 0, (void *)&r, &rl); // this reciver as parent
            buf[n] = 0;

            if (strcmp(buf, id) == 0) continue;

            int found = 0;
            for (int i = 0; i < sc; i++)
                if (strcmp(seen[i], buf) == 0)
                    found = 1;

            if (!found) { //if new system process found then print
                strcpy(seen[sc++], buf);
                printf("System online: %s (from %s)\n",
                        buf, inet_ntoa(r.sin_addr));
            }
        }
    }
}
