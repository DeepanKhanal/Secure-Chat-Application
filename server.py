# Import required modules
import socket
import threading
import secrets
from tkinter import E
import el_gamal

HOST = '192.168.56.1'
PORT = 1234 # to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

#Function to choose which security method to use
def chooseMethod():
    print("---------Welcome to the ElGamal encrypted secure chat system")
    while True:
        num = input("Please enter 1 to begin: ")
        if num == '1':
            print("ElGamal encryption mode has been started")
            return num
        else:
            print("Invalid input. Please enter 1.")

def getMethod():
    return flagmethod

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username,key,elgamapublickey,rsa_string):
    while 1:

        message = client.recv(2048).decode('utf-8')
        print("RECV : ",message)
        if message != '':
            ####### send
            final_msg = username + '~' + message + '~' + key + "~" +flagmethod+"~"+elgamapublickey+"~"+rsa_string
            send_messages_to_all(final_msg)
            print("rsaaaaaaa:   ",final_msg)

        else:
            print(f"The message send from client {username} is empty")

# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())
    print("SEND : ", message.encode() )

# Function to send any new message to all the clients
def send_messages_to_all(message):
    for user in active_clients:
        # Start the security phase using message then pass the message to client
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client,key):
    # Server will listen for client message that will contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        print("RECV : ",username)
        if username != '':
            active_clients.append((username, client,key))
            # generate session key
            key = secrets.token_hex(8).upper()

            string_ints = [str(x) for x in ElgamalKey]
            elgamalpublickey = ",".join(string_ints)
            print("elgamal public key",elgamalpublickey)

            rsa_string = ""

            #########send
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" +flagmethod +"~" + elgamalpublickey +"~"+rsa_string
            send_messages_to_all(prompt_message)

            print("Sessison key successfully generated for " + f"{username } ==>",key)

            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, key,elgamalpublickey,rsa_string, )).start()


# Main function
def main():
    global ElgamalKey
    ElgamalKey = el_gamal.generate_public_key()
    # Creating the socket class object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #choose method
    global flagmethod
    flagmethod = chooseMethod()

    # Creating a try catch block
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        key = ""
        threading.Thread(target=client_handler, args=(client,key, )).start()


if __name__ == '__main__':
    main()