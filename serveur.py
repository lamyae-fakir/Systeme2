import socket,select

HOST = "127.0.0.1" # or 'localhost' or '' - Standard loopback interface address
PORT = 2000 # Port to listen on (non-privileged ports are > 1023)
MAXBYTES = 4096



# create socket
serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    # AF_INET: IPv4
    # SOCK_STREAM: TCP


serversocket.bind((HOST, PORT)) # bind this socket to specific port on host
serversocket.listen() # make the socket a listening one
#(clientsocket,(addr,port,),) = serversocket.accept() # blocking; returns if a client connects.
socketlist = [serversocket]



while len(socketlist) > 0:
    (readable, _, _) = select.select(socketlist, [], [])
    for s in readable:
        print("desc", s.fileno())
        if s == serversocket: # serversocket receives a connection
            (clientsocket, (addr, port)) = s.accept()
            print("connection from:", port)
            socketlist.append(clientsocket)
        else: # data is sent from given client
            data = s.recv(MAXBYTES)
            if len(data) > 0:
                s.sendall(data)
            else: # client has disconnected
                s.close()
                socketlist.remove(s)
                
serversocket.close()
