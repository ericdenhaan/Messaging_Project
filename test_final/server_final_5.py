#---------------------------------------------------------------------------------
# CPSC 3780 Project - server.py - Written By: Eric Den Haan and Adam Lefaivre
#---------------------------------------------------------------------------------

import socket
import sys

#---------------------------------------------------------------------------------
# Server Address Info and Global Variables
#---------------------------------------------------------------------------------

#lookup table of server addresses and ports
server_address_1 = "142.66.140.21"
server_port_1    = 1025
server_address_2 = "142.66.140.22"
server_port_2    = 1026
server_address_3 = "142.66.140.23"
server_port_3    = 1027
server_address_4 = "142.66.140.24"
server_port_4    = 1028
server_address_5 = "142.66.140.25"
server_port_5    = 1029

#fill the list
server_port_and_address_list = []
server_port_and_address_list.append([server_address_1,server_port_1])
server_port_and_address_list.append([server_address_2,server_port_2])
server_port_and_address_list.append([server_address_3,server_port_3])
server_port_and_address_list.append([server_address_4,server_port_4])
server_port_and_address_list.append([server_address_5,server_port_5])

#map the server address & port to the host
host_address = server_address_5
host_port = server_port_5

#create the server socket and bind it to the host address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host_address, host_port))

#initialize a list of messages
message_list = []

#initialize the sequence number to 0
sequence_number = 0

#each server has a list that will contain the two-tuple: (clientID, serverAddress)
#this is used to determine which servers are serving which clients
#each server passes this list to its neighbours
server_client_list = []

#each server also has a list of messages that it must forward to other servers
messages_to_forward = []

#---------------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------------

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

#function to add a client to the client/server list
#if the client is already in the list, do nothing
#else, add it along with this server's address
def addClient(client_id):
    exists = False
    for row in server_client_list:
        if((row[0] == client_id)):
            exists = True
            break
    if(not exists):
        server_client_list.append([client_id.decode("utf-8"), host_address])
        sendList()

#function to delete a client from the client/server list
def deleteClient(client_id):
    if(server_client_list):
        for row in server_client_list:
            if((row[0] == client_id)):
                server_client_list.remove(row)
                sendList()
            
#function to parse the client/server list
#it has already been split into tuples based on each client/server pair
def parseList(incoming_split_list):
    #for each tuple of the incoming client/server list
    for row in incoming_split_list:
        exists = False
        temp_list = row.split("/")
        #compare to make sure that the server/client pair is not already in the server/client list
        for tuple in server_client_list:
            if((temp_list[0] == tuple[0])):
                exists = True
                break
        if((not exists) and (temp_list)):
            server_client_list.append([temp_list[0], temp_list[1]])
            sendList()
        
#function to exchange lists between servers
def sendList():
    string_to_send = ""
    incoming_list = []
    
    #format: client/server?client/server? etc.
    for row in server_client_list:
        string_to_send += row[0]
        string_to_send += "/"
        string_to_send += row[1]
        if(row != server_client_list[len(server_client_list) - 1]):
            string_to_send += "?"
   
    #take care of 0th index case
    if(host_port == server_port_and_address_list[0][1]):          
        #send the client/server list to the correct server (+1 only)
        server_socket.sendto(string_to_send.encode("utf-8"), 
        (server_port_and_address_list[1][0], server_port_and_address_list[1][1]))
        
    #take care of nth index case
    elif (host_port == server_port_and_address_list[len(server_port_and_address_list)-1][1]):
        #send the client/server list to the correct server (-1 only)
        server_socket.sendto(string_to_send.encode("utf-8"), 
        (server_port_and_address_list[len(server_port_and_address_list)-2][0],
        server_port_and_address_list[len(server_port_and_address_list)-2][1]))
            
    #take care of general case 
    else:
        for i in range(len(server_port_and_address_list)):
            if(server_port_and_address_list[i][1] == host_port):
                #send the client/server list to the correct server (-1/+1)
                server_socket.sendto(string_to_send.encode("utf-8"), 
                (server_port_and_address_list[i-1][0], server_port_and_address_list[i-1][1]))
                server_socket.sendto(string_to_send.encode("utf-8"), (server_port_and_address_list[i+1][0], server_port_and_address_list[i+1][1]))

#function to flood terminates to ensure the list is consistent
def forwardTerminates(received_frame):
    #set a flag to avoid feedback loops
    received_frame += "1"
    if(server_client_list):
        for tuple in server_port_and_address_list:
            if(tuple[1] != host_port):
                server_socket.sendto(received_frame.encode("utf-8"), (tuple[0], tuple[1]))

#function to forward messages to other servers
def forwardMessages():
    print("forwarding messages:")
    for message in messages_to_forward:
        dest_address = ""
        dest_port = 0
        
        #first, find the server the client belongs to, then forward to that server
        for tuple in server_client_list:
            if(tuple[0] == message[3]):
                dest_address = tuple[1]
                for i in range(len(server_port_and_address_list)):
                    if(server_port_and_address_list[i][0] == tuple[1]):
                        dest_port = server_port_and_address_list[i][1]
                        break
                forwarded_message = "/".join(message)
                if(dest_port != 0 and dest_address != "" and dest_address != host_address):
                    server_socket.sendto(forwarded_message.encode("utf-8"), (dest_address, dest_port))
                    messages_to_forward.remove(message)

#function to receive messages
def receiveMessage():
    received_frame, sender_address = server_socket.recvfrom(256)
    received_frame = received_frame.decode("utf-8")
    received_frame_list = received_frame.split("/", 4)
    print("Incoming Message: ", received_frame_list)
    return received_frame, received_frame_list, sender_address
    
#---------------------------------------------------------------------------------
# Message Routing - Program Loop
#---------------------------------------------------------------------------------
#message format: seqnum/type/source/destination/payload

print("Server is currently listening for messages from clients:")

while 1:
    #print the server/client list
    if(server_client_list):
        print("The current server/client list:")
        print(server_client_list)
    else:
        print("There are no clients attached to the servers.")
        
    #flag to avoid feedback loops with server/client list exchange
    send_list = True
    
    #if a message comes in, determine its type by examining the type field
    received_frame = ""
    received_frame_list = []
    sender_address = ""
    received_frame, received_frame_list, sender_address = receiveMessage()
    
    #if we get a list message, parse the list
    if(received_frame[2].isdigit()):
        send_list = False
        incoming_split_list = received_frame.split("?")
        parseList(incoming_split_list)
    
    #if the message is send, store the message in message_list
    if(received_frame_list[1] == "send"):
        exists = False
        message_list.append((str(sequence_number), received_frame_list[1],
        received_frame_list[2], received_frame_list[3], received_frame_list[4]))
        
        #do not store forwarded messages in messages_to_forward
        for row in server_client_list:
            if(received_frame_list[3] == row[0]):
                if(row[1] != host_address):
                    messages_to_forward.append((str(sequence_number), received_frame_list[1],
                    received_frame_list[2], received_frame_list[3], received_frame_list[4]))

        #also, add the source to the client/server list
        addClient(received_frame_list[2])

        #increment sequence number, if it reaches 100, roll over to 0
        sequence_number += 1
        if(sequence_number == 100):
            sequence_number = 0

    #if the message is get, look through stored messages
    #send those that have the correct client in destination field
    #if there is nothing, send a dummy message
    if(received_frame_list[1] == "get"):
        #add the source to the client/server list
        addClient(received_frame_list[2])
        response = findMessage(received_frame_list[2], message_list)	
        if(response != None):
            response = "/".join(response)
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))     
        else:
            response = "1/send/server/" + received_frame_list[2] + "/"
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))
    
    #when we get the ack for a stored message, we delete the message
    if(received_frame_list[1] == "ack"):
            removeMessage(received_frame_list[0], message_list)

    #if we get a terminate message, delete the client/server tuple from the table
    #if the flag is not 1, then we can flood the terminate to all servers
    if(received_frame_list[1] == "terminate"):
        if(received_frame_list[4] == "1"):
            deleteClient(received_frame_list[2])
        else:
            forwardTerminates(received_frame)
            deleteClient(received_frame_list[2])
            
    if(received_frame_list[1] == "handshake"):
        addClient(received_frame_list[2])
        sendList()
    
    #print the list of messages to send and messages to forward
    print("messages to forward:")
    print(messages_to_forward)
    print("message list:")
    print(message_list)
    
    #forward messages if there are any to forward
    if(messages_to_forward):
        forwardMessages()

