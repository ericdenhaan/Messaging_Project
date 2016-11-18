import socket
import sys

#host(server) address
host_address = "localhost"
#host(server) port
host_port = 2000

#create the server socket and bind it to the host address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host_address, host_port))

#initialize the sequence number to 0
sequence_number = 0

#initialize a list of messages
message_list = []

#function to send a message to a client
def findMessage(destination, list):
    for received_frame in list:
        if(received_frame[3] == destination):
            return received_frame

#function to remove a buffered message
def removeMessage(sequence_number, list):
    for received_frame in list:
        if(received_frame[0] == sequence_number):
            list.remove(received_frame)
    
#put the server in listen mode, and wait for messages from clients
print("Server is currently listening for messages from clients:")

while 1:
    #if a message comes in, determine its type by examining the type field
    received_frame, sender_address = server_socket.recvfrom(256)
    received_frame = received_frame.decode("utf-8")
    received_frame = received_frame.split("/")
    print("Incoming Message: ", received_frame)

    #if the message is send, store the message
    if(received_frame[1] == "send"):
        message_list.append((str(sequence_number), received_frame[1],
        received_frame[2], received_frame[3], received_frame[4]))
        #increment sequence number, if it reaches 100, roll over to 0
        sequence_number += 1
        if(sequence_number == 100):
            sequence_number = 0
        
    #if the message is get, look through stored messages    #send those that have the correct client in destination field
    if(received_frame[1] == "get"):
        response = findMessage(received_frame[2], message_list)	
        if(response != None):
            response = "/".join(response)
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))     
        else:
            response = "1/send/server/" + received_frame[2] + "/"
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))
    
    #when we get the ack for a stored message, we delete the message
    if(received_frame[1] == "ack"):
        removeMessage(received_frame[0], message_list)
        