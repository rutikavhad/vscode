#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

int main() {
    char hostbuffer[256];
    char *IPbuffer;
    struct hostent *host_entry;

    // Step 1: Get local system hostname (like "mycomputer" or "ubuntu")
    if (gethostname(hostbuffer, sizeof(hostbuffer)) == -1) {
        perror("gethostname");
        return 1;
    }

    // Step 2: Get information about the host (IP addresses, etc.)
    host_entry = gethostbyname(hostbuffer);
    if (host_entry == NULL) {
        perror("gethostbyname");
        return 1;
    }

    // Step 3: Convert first IP address to readable form (string)
    IPbuffer = inet_ntoa(*((struct in_addr*) host_entry->h_addr_list[0]));

    // Step 4: Print the IP address only
    printf("Local IP Address: %s\n", IPbuffer);
    return 0;
}
