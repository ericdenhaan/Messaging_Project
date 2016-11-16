#CPSC 3780
#Project
#Written By: Adam Lefaivre and Eric Den Haan
#Test file, working through tutorial found at:
#http://www.ibm.com/developerworks/linux/tutorials/l-pysocks/index.html

#First step: import the sockets library
import socket

#create a datagram (UDP) socket
#AF_INET = IPv4 socket, SOCK_DGRAM = datagram socket
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#close a socket
udpSocket.close()

#delete a socket
del udpSocket

#creating datagram server sockets:
#endpoint address for a socket: ('interface address', port number)
#bind function will bind the socket to this address
#there is no 'accept' method for accepting new connections as UDP is connectionless
#socket creation same as before
udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#binding the socket: '' means that any incoming connection will be allowed
#2525 means that the socket is bound to port 2525
udpServerSocket.bind(('', 2525))

#creating datagram client sockets:
#this creates a UDP client socket, and connects it to a server at 192.168.1.1
#we could also make the server address a variable and specify it with the message
#when we send it
udpClientSocket = socket.socket(AF_INET, socket.SOCK_DGRAM)

#connect function specifies where the messages are going to go
udpClientSocket.connect(('192.168.1.1', 2525))