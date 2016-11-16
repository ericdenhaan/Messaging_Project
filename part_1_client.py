import socket
import sys

#server address
#client address
#server port
#client port

#create the socket
#bind the socket to the client address and port

#get this client's ID

#options:#send a message to the other client

#send a get request to the server to pick up messages

#create the message (based on the option given)
#message format:
#seq. no
#type (send or get)
#source (ID for this client)
#dest (ID for the other client)
#payload (the message)
#send it to the server#wait for either the get result from the server
#or for the ack from the other client