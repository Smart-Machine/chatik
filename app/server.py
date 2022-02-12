#! /usr/bin/python

import socket 
import threading 
from constants import *

CONNECTIONS = []
NICKNAMES = {}

def handle_clients(connection: socket.socket, address: str) -> None:
    while True:
        try:
            message = connection.recv(BUFSIZE).decode()

            if address[1] not in NICKNAMES and message.split()[0] == 'Name':
                NICKNAMES[address[1]] = message.split()[2] 
                print(INFO + f'{address[0]}:{address[1]} connected as {NICKNAMES[address[1]]}')
                broadcast(INFO + f'{NICKNAMES[address[1]]} joined the chat.', connection, address)

            elif message == 'quit()' or message == 'exit()':
                print(INFO + f'Disconnected {NICKNAMES[address[1]]}.')
                broadcast(INFO + f'{NICKNAMES[address[1]]} left chat.', connection, address)
                
                message_to_sent = 'QUIT'
                connection.send(message_to_sent.encode())
                remove_connection(connection, address)
                break

            else: 
                if message:
                    print(LOG + f'From {NICKNAMES[address[1]]} -> {message}')

                    message_to_sent = f'{USER}[{NICKNAMES[address[1]]}]{RESET}:: {message}'
                    broadcast(message_to_sent, connection, address)

                else:
                    remove_connection(connection, address)
                    break

        except Exception as e:
            print(ERROR + f'Error when handling user connection: {e}')
            remove_connection(connection, address)
            break


def broadcast(message: str, connection: socket.socket, address: str) -> None:
    for client_connection in CONNECTIONS:
        if client_connection != connection:
            try:
                client_connection.send(message.encode())
            
            except Exception as e:
                print(ERROR + f'Error when broadcasting message: {e}')
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

        print(f'{colorama.Fore.GREEN}[ Server started. ]{colorama.Style.RESET_ALL}')

        while True:
            try:
                connection, address = server.accept()
            except:
                print(f'\n{colorama.Fore.GREEN}[ Server stoped ]{colorama.Style.RESET_ALL}')
                break
            CONNECTIONS.append(connection)
            threading.Thread(target=handle_clients, args=(connection, address)).start()
    
    except Exception as e:
        print(ERROR + f'An error has occured when starting the server: {e}')
    
    finally:
        if len(CONNECTIONS) > 0:
            for connection in CONNECTIONS:
                remove_connection(connection, address)
        server.close()


if __name__ == '__main__':
    start_server()
