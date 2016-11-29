#---------------------------------------------------------------------------------
# CPSC 3780 Project - client_final.py - Written By: Eric Den Haan and Adam Lefaivre
#---------------------------------------------------------------------------------

import socket
import sys

#---------------------------------------------------------------------------------
# Client Address Info and Global Variables
#---------------------------------------------------------------------------------

#client address
client_address = "142.66.140.21"
#client port
client_port = input("Please enter a port (2100 or 2200?): ")

#create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind the socket to the client address and port
client_socket.bind((client_address, client_port))

#initialize the ack_check variable
ack_check = False

while 1:
    #get this client's ID
    source = raw_input("Please enter a 10 digit ID: ")
    if(len(source) != 10):
        print("Sorry, ID must be 10 digits. Please try again: ")
    else:
        break
       
while 1:
    #get this client's corresponding server and assign address and port
    serverID = input("Please enter the server you want to use for this client (1 to 5): ")
    if ((serverID >= 1) and (serverID <= 5)):
        if(serverID == 1):
            server_address = "142.66.140.21"
            server_port = 1025 				
        if(serverID == 2):
            server_address = "142.66.140.22"
            server_port = 1026		
        if(serverID == 3):
            server_address = "142.66.140.23"
            server_port = 1027 		                            
        if(serverID == 4):
            server_address = "142.66.140.24"
            server_port = 1028	                
        if(serverID == 5):		
            server_address = "142.66.140.25"
            server_port = 1029		                			
        break
    else:
        print("Sorry, the server must be from 1 to 5!  Try again.")
        
#send an initial handshake to get the server/client list set up
handshake = "1/handshake/"+source+"//"
client_socket.sendto(handshake.encode("utf-8"), (server_address, server_port))

#---------------------------------------------------------------------------------
# Program Loop
#---------------------------------------------------------------------------------

while 1:    
    #create an empty message
    message = ""
            
    #program options:    
    option = input("Press 1 to send a message,\nPress 2 to receive messages,\nPress 3 to quit: ")
    
    #send a message to the other client
    if(option == 1):
        #create the message (based on the option given)      
        #seq. no
        message += "1"
        message += "/"      
        #type (send or get)
        message += "send"
        message += "/"      
        #source (ID for this client)
        message += source
        message += "/"      
        #destination (ID for the other client)
        while 1:
            destination = raw_input("Please enter the destination client's 10 digit ID: ")
            if(len(destination) != 10):
                print("Sorry, ID must be 10 digits. Please try again: ")
            else:
                break
        message += destination
        message += "/"
        #payload
        while 1:
            payload = raw_input("Please enter the message (max 160 characters): ")
            if(len(payload) > 160):
                print("Sorry, message must be <= 160 characters. Please try again: ")
            else:
                break
        message += payload
        
        #send the message
        client_socket.sendto(message.encode("utf-8"), (server_address, server_port))
        print("Message sent!")
    
    elif(option == 2):
        #create the message (based on the option given)
        #message format:
        #seq. no
        message += "1"
        message += "/"
        #type (send or get)
        message += "get"
        message += "/"
        #source (ID for this client)
        message += source
        message += "/"
        #remaining fields will be empty
        message += ""
        message += "/"
        message += ""
        
        #while there are unread messages for this client on the server
        count = 0
        while 1:      
            while count < 6:            
                #send the get request
                client_socket.sendto(message.encode("utf-8"), (server_address, server_port))
                
                #process the reply (buffer 256 bits, decode the string, and split it into a list)
                received_frame, sender_address = client_socket.recvfrom(256)
                received_frame = received_frame.decode("utf-8")
                received_frame_list = received_frame.split('/', 4)
            
                if(received_frame[4] != ""):
                    count = 0
                    break
                else:
                    count += 1

            #if no messages left, break, else display the message
            if(received_frame_list[4] == ""):
                if(ack_check == True):
                    pass 
                else:
                    print("The server has no messages for you.")
                ack_check = False
                break
            else:
                print("Message received from " + received_frame_list[2] + ": " + received_frame_list[4])
                ack_check = True
                
            #send an acknowledgement
            ack = received_frame_list[0] + "/ack/" + source + "/" + received_frame_list[2] + "/" + received_frame_list[4]
            client_socket.sendto(ack.encode("utf-8"), (server_address, server_port))
            
    else:
        print("Goodbye.")
        #send a terminate message to the server to make the server remove any info for this client
        terminate = "0/terminate/" + source + "//"
        client_socket.sendto(terminate.encode("utf-8"), (server_address, server_port))
        #close the connection and the program
        client_socket.close()
        sys.exit(0)
        
