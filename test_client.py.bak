#CPSC 3780
#Project
#Written By: Adam Lefaivre and Eric Den Haan
#Test echo client file, working through tutorial found at:
#http://www.ibm.com/developerworks/linux/tutorials/l-pysocks/index.html

import socket

#initialize a datagram socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#send a message to a specific address using sendto function
clientSocket.sendto("Hello\n",('',23000))

#print the response using recv function
print clientSocket.recv(100)

#close the socket
clientSocket.close()