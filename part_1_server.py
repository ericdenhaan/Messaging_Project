from twisted.internet import task
from twisted.internet import reactor
import socket
import sys

#---------------------------------------------------------------------------------
# Basic Server Info
#---------------------------------------------------------------------------------

#Table of Server Addresses and Ports (reassign values)
server_address_1 = "localhost"
server_port_1    = 1025
server_address_2 = "localhost"
server_port_2    = 1026
server_address_3 = "localhost"
server_port_3    = 1027
server_address_4 = "localhost"
server_port_4    = 1028
server_address_5 = "localhost"
server_port_5    = 1029

server_port_and_address_list = []
server_port_and_address_list.append([server_port_1,server_address_1])
server_port_and_address_list.append([server_port_2,server_address_2])
server_port_and_address_list.append([server_port_3,server_address_3])
server_port_and_address_list.append([server_port_4,server_address_4])
server_port_and_address_list.append([server_port_5,server_address_5])

# Map the server address & port to the host(reassign values)
host_address = server_address_1
host_port = server_port_1

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

#---------------------------------------------------------------------------------
# Distance Vector Routing Implementation
#---------------------------------------------------------------------------------

#Each server list will contain the two-tuple: (clientID, serverAddress),
#periodically, messages will be forwarded to the correct server and 
#the client ID with the different server will be deleted.
thisServerClientList = []
thisForwardingList = []

def addClientToThisServerList(clientID):
    for serverClientListRow in thisServerClientList:
        if((serverClientListRow[0] == clientID))
            exists = True
            break;
        if(!exists):
            thisServerClientList.append([clientID, host_address])

def parseIncomingClientList(incomingClientServerArray):
    incomingClient = ""
    incomingServer = ""
    for i in len(incomingClientServerArray):
        incomingClient = incomingClientServerArray[i]	
        incomingServer = incomingClientServerArray[i + 1]
        if(incomingServer == host_address):
            addClientToThisServerList(incomingClient)
        else:
		    #TODO CHECK THIS WITH ERIC TOMORROW
            #DO FORWARDING HERE??????????????
            #loop through server_port_and_address_list to find server address and forward client
            for portAdressTuple in server_port_and_address_list:
                if(portAdressTuple[1] == incomingClientServerArray[i + 1]):
                    server_socket.sendto(clientListAsString.encode("utf-8"), (portAdressTuple[0], portAdressTuple[1]))
		
    
		
				
def exchangeListsBetweenServers():
    shouldIncomingClientListBeParsed = False
    stringToSend = ""
    incomingClientServerArray = []
    for row in thisServerClientList:
        stringToSend += row[0]
        stringToSend += "/"
        stringToSend += row[1]	
        stringToSend += "/"

    #Receive & Send data from server +/- 1
    #---------------------------------------
    incomingServerClientList, sender_address = server_socket.recvfrom(256)
	
	#Take care of 0th index case
    if(host_port == server_port_and_address_list[0][0]):
        if(server_port_and_address_list[1][1] == sender_address):
            shouldIncomingClientListBeParsed = True    
        
        server_socket.sendto(stringToSend.encode("utf-8"), (server_port_and_address_list[1][0], server_port_and_address_list[1][1]))        
		
    #Take care of nth index case
	else if (host_port == server_port_and_address_list[len(server_port_and_address_list)][0]):
        if(server_port_and_address_list[len(server_port_and_address_list) - 1][1] == sender_address):
            shouldIncomingClientListBeParsed = True
        
        server_socket.sendto(stringToSend.encode("utf-8"), (server_port_and_address_list[len(server_port_and_address_list) - 1][0], len(server_port_and_address_list) - 1][1]))
			
    #Take care of general case 
    else:
        for i in len(server_port_and_address_list):
		    if(server_port_and_address_list[i][0] == host_port):
			    if((server_port_and_address_list[i-1][1] == sender_address) or 
                  (server_port_and_address_list[i+1][1])):
                    shouldIncomingClientListBeParsed = True	

                server_socket.sendto(stringToSend.encode("utf-8"), (server_port_and_address_list[i - 1][0], server_port_and_address_list[i - 1][1]))
                server_socket.sendto(stringToSend.encode("utf-8"), (server_port_and_address_list[i + 1][0], server_port_and_address_list[i + 1][1]))
                				

    if(shouldIncomingClientListBeParsed):
        incomingServerClientList = incomingServerClientList.decode("utf-8")
        incomingClientServerArray = incomingServerClientList.split('/')
        

#Run the exchange lists function occasionally 
timeout = 2.0
exchangeLists = task.LoopingCall(exchangeListsBetweenServers)
timeout.start(timeout) # call every two seconds
reactor.run()
	
#---------------------------------------------------------------------------------
# Message Routing
#---------------------------------------------------------------------------------
#seqnum/type/source/destination/payload

#put the server in listen mode, and wait for messages from clients
print("Server is currently listening for messages from clients:")

while 1:
    #if a message comes in, determine its type by examining the type field
    received_frame, sender_address = server_socket.recvfrom(256)
    received_frame = received_frame.decode("utf-8")
    received_frame_list = received_frame.split('/', 4)
    print("Incoming Message: ", received_frame_list)

    #if the message is send, store the message
    if(received_frame_list[1] == "send"):
        message_list.append((str(sequence_number), received_frame_list[1],
        received_frame_list[2], received_frame_list[3], received_frame_list[4]))
		
        addClientToServerList(received_frame_list[2])
        
		#increment sequence number, if it reaches 100, roll over to 0
        sequence_number += 1
        if(sequence_number == 100):
            sequence_number = 0
        
    #if the message is get, look through stored messages    #send those that have the correct client in destination field
    if(received_frame_list[1] == "get"):
        response = findMessage(received_frame_list[2], message_list)	
        if(response != None):
            response = "/".join(response)
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))     
        else:
            response = "1/send/server/" + received_frame_list[2] + "/"
            server_socket.sendto(response.encode("utf-8"), (sender_address[0], sender_address[1]))
			
		addClientToServerList(received_frame_list[2])
		 
    #when we get the ack for a stored message, we delete the message
    if(received_frame_list[1] == "ack"):
        removeMessage(received_frame_list[0], message_list)
        