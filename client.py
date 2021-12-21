#! /usr/bin/python

import socket, threading, rsa, random, textwrap 
from constants import *


def handle_messages(connection: socket.socket) -> None:
    
    while True:

        try:
            message = connection.recv(BUFSIZE).decode()

            wrapper = textwrap.TextWrapper(width=50)
            word_list = wrapper.wrap(text=message)

            if message == 'QUIT':
                break
            elif message:
                #print(message)
                for word in word_list:
                    print(word)
            else:
                connection.close()
                break
        
        except Exception as e:
            print(ERROR + f'Error when handling messages from server: {e}')
            connection.close()
            break


def start_chat() -> None:

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.connect((HOST, PORT))
        threading.Thread(target=handle_messages, args=(client,)).start()

        while True:
            nickname = input(INFO + 'Name : ')
            if nickname:
                client.send(('Name : ' + nickname).encode())
                break
            else :
                print(ERROR + 'Enter your name.')

        print(INFO + f'Joined the chat.')

        while True:
            message = input()

            client.send(message.encode())

            if message == 'quit()' or message == 'exit()':
                break

        client.close()
        print(INFO + f'Quited the chat.')
    
    except Exception as e:
        print(ERROR + f'Error has occured when connecting to the server: {e}')
        client.close()


if __name__ == '__main__':

    start_chat()
