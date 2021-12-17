#! /usr/bin/python

import socket, threading

HOST, PORT = 'localhost', 65432
BUFSIZE = 1024
CONNECTIONS = []
NICKNAMES = {}

def handle_clients(connection: socket.socket, address: str) -> None:

    while True:

        try:
            message = connection.recv(BUFSIZE)

            if address[1] not in NICKNAMES and message.decode().split()[0] == 'Name':
                NICKNAMES[address[1]] = message.decode().split()[2] 
                print(f'{address[0]}:{address[1]} connected as {NICKNAMES[address[1]]}')
                broadcast(f'{NICKNAMES[address[1]]} joined the chat.', connection, address)
            elif message.decode() == 'quit()' or message.decode() == 'exit()':
                print(f'Disconnecting {NICKNAMES[address[1]]}.')
                broadcast(f'{NICKNAMES[address[1]]} left chat.', connection, address)
                
                message_to_sent = 'QUIT'
                connection.send(message_to_sent.encode())
                remove_connection(connection, address)
                break
            else: 
                if message:
                    print(f'From {NICKNAMES[address[1]]} -> {message.decode()}')

                    message_to_sent = f'{NICKNAMES[address[1]]} :: {message.decode()}'
                    broadcast(message_to_sent, connection, address)
                else:
                    remove_connection(connection, address)
                    break

        except Exception as e:
            print(f'Error when handling user connection: {e}')
            remove_connection(connection, address)
            break

def broadcast(message: str, connection: socket.socket, address: str) -> None:

    for client_connection in CONNECTIONS:
        if client_connection != connection:

            try:
                client_connection.send(message.encode())
            
            except Exception as e:
                print(f'Error when broadcasting message: {e}')
                remove_connection(client_connection, address)

def remove_connection(connection: socket.socket, address: str) -> None:
    
    if address in NICKNAMES:
        del NICKNAMES[address[1]]
   
    if connection in CONNECTIONS:
        connection.close()
        CONNECTIONS.remove(connection)
   
def start_server() -> None:
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print('[ Server started. ]')

        while True:
            try:
                connection, address = server.accept()
            except:
                print(f'\n[ Server stoped ]')
                break
            CONNECTIONS.append(connection)
            threading.Thread(target=handle_clients, args=(connection, address)).start()
    
    except Exception as e:
        print(f'An error has occured when starting the server: {e}')
    
    finally:
        if len(CONNECTIONS) > 0:
            for connection in CONNECTIONS:
                remove_connection(connection, address)
        server.close()

if __name__ == '__main__':
    start_server()