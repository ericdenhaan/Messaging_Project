#CPSC 3780
#Project
#Written By: Adam Lefaivre and Eric Den Haan

#import the sockets library
import socket

#create a datagram (UDP) socket
#AF_INET = IPv4 socket, SOCK_DGRAM = datagram socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#close a socket
udpSocket.close()

#delete a socket
del udpSocket