import threading
from socket import*


#host='192.168.56.1'
port= 12345

server_socket=socket(AF_INET,SOCK_STREAM)
server_socket.bind(('',port))
server_socket.listen(5)

clients=[]
admin=[]
names=[]
banned_names=[]

def broadcast(message):
    for client in clients:
        client.send(message)

    
def print_client():
     for a in admin:
        a.send("Current Clients In The Chat Room:".encode('ascii'))
        for i in names:
            a.send(i.encode('ascii'))
            a.send(" ".encode('ascii'))


def handle_client(client):
    while True:
        try:
            msg=message=client.recv(2048)
            if(msg.decode('ascii').startswith('KICK')):
                if(names[clients.index(client)]=="admin" or names[clients.index(client)]=="Admin"):
                    name_to_kick=msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("Command cannot be executed!!".encode('ascii'))
            elif(msg.decode('ascii').startswith('BAN')):
                if(names[clients.index(client)]=="admin" or names[clients.index(client)]=="Admin"):
                    name_to_ban=msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    banned_names.append(name_to_ban)
                    print(f'{name_to_ban} was banned!!')
                else:
                    client.send("Command cannot be executed!!".encode('ascii'))

            else:
                 broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=names[index]
            broadcast(f'{nickname} has left the chat!!'.encode('ascii'))
            names.remove(nickname)
            break
def receive():
    while True:
        client,client_addr=server_socket.accept()
        print("Connected with address:",client_addr)

        client.send("NICK:".encode('ascii'))
        nickname=client.recv(2048).decode('ascii')

        if nickname in banned_names:
            client.send("BAN".encode('ascii'))
            client.close()
            continue

        if nickname=='admin':
            client.send("PASS".encode('ascii'))
            password=client.recv(1024).decode('ascii')

            if password!='boss@123':
                client.send("REJECTED".encode('ascii'))
                client.close()
                continue

        if(nickname=='admin'):
            admin.append(client)


        names.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has joined the chat!!'.encode('ascii'))
        client.send("Connected to the server!!".encode('ascii'))
        if admin!=[]:
            print_client()
        
        t1=threading.Thread(target=handle_client,args=(client,))
        t1.start()


def kick_user(name):
    name_index=names.index(name)
    client_to_kick=clients[name_index]
    clients.remove(client_to_kick)
    client_to_kick.send("You were kicked by the admin!!".encode('ascii'))
    client_to_kick.close()
    names.remove(name)
    broadcast(f'{name} was kicked by the admin!'.encode('ascii'))
    print_client()


print("Server is listening..!!")
receive()


