import socket 
s=socket.socket()
print('socket crée ')
port = 56789
s.bind(('', port))
print(f'socket binded au port {port}')
s.listen(5)
print("socket is listening")
while True:
    c,addr =s.accept()
    print = ('connexion a partir de ', addr)
    message = ('merci pour la connexion')
    c.send(message.encode())
    c.close()