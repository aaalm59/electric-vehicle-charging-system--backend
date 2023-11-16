#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <unistd.h>

#include <sys/types.h>

#include <sys/socket.h>

#include <netinet/in.h>

#include <netdb.h>

#define SA struct sockadd

int main(int argc, char *argv[]) {

    int sockfd, portno, n, connfd, len;

    struct sockaddr_in serv_addr, cli;

    struct hostent *server;



    char buffer[256];
    char buffer1[1024];

    if (argc < 3) {

        fprintf(stderr, "usage %s hostname port\n", argv[0]);

        exit(0);

    }



    portno = atoi(argv[2]);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0) {

        perror("ERROR opening socket");

        exit(1);

    }



    server = gethostbyname(argv[1]);

    if (server == NULL) {

        fprintf(stderr,"ERROR, no such host\n");

        exit(0);

    }



    memset((char *) &serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;

    serv_addr.sin_port = htons(portno);

    memcpy(&serv_addr.sin_addr.s_addr, server->h_addr, server->h_length);



    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) {

        perror("ERROR connecting");

        exit(1);

    }



    printf("Please enter the message: ");

    memset(buffer, 0, 256);

    fgets(buffer, 255, stdin);



    n = write(sockfd, buffer, strlen(buffer));

    if (n < 0) {

        perror("ERROR writing to socket");

        exit(1);

    }
    //func(connfd);    

    bzero(buffer1, 1024);
   // read(sockfd, buffer, sizeof(buffer));
    int numbytes = recv(sockfd, buffer1, 1024,0);
    // print buffer which contains the client contents
    printf("received %d bytes: %s\n", numbytes, buffer1);

    close(sockfd);
    return 0;

}
