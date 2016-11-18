import socket
import sys

#server address
server_address = "localhost"
#client address
client_address = "localhost"
#server port
server_port = 2000
#client port
client_port = input("Please enter a port (2100 or 2200?): ")

#create the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#bind the socket to the client address and port
client_socket.bind((client_address, client_port))

#initialize sequence number to 0
sequence_number = 0

while 1:
    #get this client's ID
    source = raw_input("Please enter a 10 digit ID: ")
    if(len(source) != 10):
        print("Sorry, ID must be 10 digits. Please try again: ")
    else:
        break

while 1:    
    #create an empty message
    message = ""
    
    #increment sequence number, if it reaches 100, roll over to 0
    sequence_number += 1
    if(sequence_number == 100):
        sequence_number = 0
        
    #program options:    
    option = input("Press 1 to send a message,\nPress 2 to receive messages,\nPress 3 to quit: ")
    
    #send a message to the other client
    if(option == 1):
        #create the message (based on the option given)      
        #seq. no
        message += str(sequence_number)
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
            #remove any '/' characters so they do not interfere with splitting later
            destination = destination.replace("/","")
            if(len(destination) != 10):
                print("Sorry, ID must be 10 digits. Please try again: ")
            else:
                break
        message += destination
        message += "/"
        #payload
        while 1:
            payload = raw_input("Please enter the message (max 160 characters): ")
            #remove "/" characters so they do not interfere with splitting later
            payload = payload.replace("/", "")
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
        message += str(sequence_number)
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
        while 1:
            #send the get request
            client_socket.sendto(message.encode("utf-8"), (server_address, server_port))
            
            #process the reply (buffer 256 bits, decode the string, and split it into a list)
            received_frame, sender_address = client_socket.recvfrom(256)
            received_frame = received_frame.decode("utf-8")
            received_frame = received_frame.split("/")
            
            #if no messages left, break, else display the message
            if(received_frame[4] == ""):
                print("The server has no messages for you.")
                break
            else:
                print("Message received from " + received_frame[2] + ":" + received_frame[4])
            
            #send an acknowledgement
            ack = received_frame[0] + "/ack/" + source + "/" + received_frame[2] + "/" + received_frame[4]
            client_socket.sendto(ack.encode("utf-8"), (server_address, server_port))
            
    else:
        print("Goodbye.")
        #close the connection and the program
        client_socket.close()
        sys.exit(0)
        