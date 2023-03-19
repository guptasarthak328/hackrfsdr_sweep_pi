## https://pythontic.com/modules/socket/udp-client-server-example ##

import socket
import sys

localIP     = sys.argv[2] #SERVER IP ADDRESS

localPort   =  int(sys.argv[1]) #PORT NUMBER

bufferSize  = int(sys.argv[3]) #VECTOR LENGTH
 
msgFromServer       = "Hello UDP Client"

bytesToSend         = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # Create a datagram socket

UDPServerSocket.bind((localIP, localPort)) # Bind to address and ip

print("UDP server up and listening")

while(True): # Listen for incoming datagrams

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address) 
    
    print(clientMsg) 
    print(clientIP) #This line can be commented

    UDPServerSocket.sendto(bytesToSend, address)  # Sending a reply to client (Raspberry Pi)
