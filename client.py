#! /usr/bin/python

import socket, threading

HOST, PORT = 'localhost', 65432
BUFSIZE = 1024

def handle_messages(connection: socket.socket) -> None:
    
    while True:

        try:
            message = connection.recv(BUFSIZE)

            if message.decode() == 'QUIT':
                break
            elif message:
                print(message.decode())
            else:
                connection.close()
                break
        
        except Exception as e:
            print(f'Error when handling messages from server: {e}')
            connection.close()
            break

def start_chat() -> None:

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.connect((HOST, PORT))
        threading.Thread(target=handle_messages, args=(client,)).start()


        nickname = input('Name : ')
        client.send(('Name : ' + nickname).encode())

        print(f'Joined the chat.')

        while True:
            message = input()
            client.send(message.encode())

            if message == 'quit()' or message == 'exit()':
                break

        client.close()
        print(f'Quited the chat.')
    
    except Exception as e:
        print(f'Error has occured when connecting to the server: {e}')
        client.close()

if __name__ == '__main__':
    start_chat()
