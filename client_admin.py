import socket
import threading
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.145.151', 12345))
stop_thread = False
nickname = input("Enter You name:")
if nickname == 'admin' or nickname=='Admin':
    password = input("Enter the password:")


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if(message == "NICK:"):
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REJECTED':
                        print("Connection Was Refused ! Wrong Password")
                        stop_thread = True
                elif next_message=="BAN":
                    print("Connection is refused because you were banned!")
                    client.close()
                    stop_thread=True

            else:
                print(message)
        except:
            print('Some Error occurred')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/KICK'):
                    client.send(
                        f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/BAN'):
                    client.send(
                        f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))

            else:
                print("Commands can only be executed by admin!!")
        else:
            client.send(message.encode('ascii'))


recieve_thread = threading.Thread(target=receive)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
