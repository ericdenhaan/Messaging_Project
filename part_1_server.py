import socket
import sys

#host(server) address
#host(server) port

#put the server in listen mode, and wait for messages from clients

#if a message comes in, determine its type by examining the type field
#if the message is get, look through stored messages#send those that have the correct client in destination field

#if the message is send, store the message#when we get the ack for this stored message, we delete the message
#and forward the ack to the client