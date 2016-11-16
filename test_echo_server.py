#CPSC 3780
#Project
#Written By: Adam Lefaivre and Eric Den Haan
#Test echo server file, working through tutorial found at:
#http://www.ibm.com/developerworks/linux/tutorials/l-pysocks/index.html

import socket

#initialize a datagram socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#bind the socket to any incoming address and port 23000
serverSocket.bind(('', 23000))

#start an infinite loop for serving client requests
while 1:
#recvfrom function receives a message from the datagram socket
#returns message and source of message
    msg,(addr,port) = serverSocket.recvfrom(100)
#sendto function returns this message back to the source
    serverSocket.sendto(msg,(addr,port))