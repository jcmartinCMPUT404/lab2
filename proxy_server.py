#!/usr/bin/env python3
from http import client
from multiprocessing.connection import Client
import socket, sys
import time
from multiprocessing import Process

HOST = ""
PORT = 80
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    try:
        # server for client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
            #QUESTION 3
            socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            #bind socket to address
            socket_client.bind((HOST, PORT))
            #set to listening mode
            socket_client.listen(2)

            #continuously listen for connections
            while True:
                conn, addr = socket_client.accept()
                print("Connected by", addr)
                p = Process(target=multi_client_handler, args=(conn, addr))
                p.daemon=True
                p.start()
                conn.close()
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        socket_client.close()

def multi_client_handler(conn, addr):
    # client for google
    #define address info, payload, and buffer size
    host = 'www.google.com'
    port = 80
    buffer_size = 4096

    #make the socket, get the ip, and connect
    #s is google
    s = create_tcp_socket()

    remote_ip = get_remote_ip(host)

    s.connect((remote_ip , port))
    print (f'Socket Connected to {host} on ip {remote_ip}')

    #recieve data, wait a bit, then send it back
    client_data = conn.recv(BUFFER_SIZE)
    
    #send client data to google
    send_data(s, client_data)
            
    #continue accepting data until no more left
    response_data = b""
    while True:
        data = s.recv(buffer_size)
        if not data:
            break
        response_data += data
    #send data back to client
    conn.sendall(response_data)

if __name__ == "__main__":
    main()