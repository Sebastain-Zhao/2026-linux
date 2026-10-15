#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static void die(const char *message) {
    perror(message);
    exit(EXIT_FAILURE);
}

static int parse_port(const char *text) {
    char *end = NULL;
    long value = strtol(text, &end, 10);
    if (!text[0] || *end || value < 1 || value > 65535) {
        fprintf(stderr, "invalid port: %s\n", text);
        exit(EXIT_FAILURE);
    }
    return (int)value;
}

static void run_server(int port) {
    int listener = socket(AF_INET, SOCK_STREAM, 0);
    if (listener < 0) die("socket");

    int reuse = 1;
    if (setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) die("setsockopt");

    struct sockaddr_in address = {
        .sin_family = AF_INET,
        .sin_port = htons((uint16_t)port),
        .sin_addr.s_addr = htonl(INADDR_LOOPBACK),
    };
    if (bind(listener, (struct sockaddr *)&address, sizeof(address)) < 0) die("bind");
    if (listen(listener, 5) < 0) die("listen");

    int connection = accept(listener, NULL, NULL);
    if (connection < 0) die("accept");
    char buffer[4096];
    ssize_t count;
    while ((count = read(connection, buffer, sizeof(buffer))) > 0) {
        ssize_t sent = 0;
        while (sent < count) {
            ssize_t result = write(connection, buffer + sent, (size_t)(count - sent));
            if (result < 0) die("write");
            sent += result;
        }
    }
    if (count < 0) die("read");
    close(connection);
    close(listener);
}

static void run_client(const char *host, int port, const char *message) {
    int connection = socket(AF_INET, SOCK_STREAM, 0);
    if (connection < 0) die("socket");
    struct sockaddr_in address = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    if (inet_pton(AF_INET, host, &address.sin_addr) != 1) {
        fprintf(stderr, "invalid IPv4 address: %s\n", host);
        exit(EXIT_FAILURE);
    }
    if (connect(connection, (struct sockaddr *)&address, sizeof(address)) < 0) die("connect");
    size_t length = strlen(message);
    if (write(connection, message, length) != (ssize_t)length) die("write");
    shutdown(connection, SHUT_WR);
    char buffer[4096];
    ssize_t count = read(connection, buffer, sizeof(buffer) - 1);
    if (count < 0) die("read");
    buffer[count] = '\0';
    puts(buffer);
    close(connection);
}

int main(int argc, char **argv) {
    if (argc == 3 && strcmp(argv[1], "server") == 0) {
        run_server(parse_port(argv[2]));
        return 0;
    }
    if (argc == 5 && strcmp(argv[1], "client") == 0) {
        run_client(argv[2], parse_port(argv[3]), argv[4]);
        return 0;
    }
    fprintf(stderr, "usage: %s server PORT | client IPV4 PORT MESSAGE\n", argv[0]);
    return EXIT_FAILURE;
}

