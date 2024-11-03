import socket
import threading
import getpass

import rsa
from hashlib import sha256

public_key, private_key = rsa.newkeys(1024)
public_partner = None
PORT = 9989

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

choice = input("Do you want to host (1) or join a chat (2): ")
password = ""

if choice == "1":
    password = getpass.getpass("Enter a password: ")
    hashed = sha256(password.encode()).hexdigest() # stored password is hashed to prevent MITM attacks
    local_ip = get_host_ip()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip, PORT)) # change IP address here (ipconfig getifaddr en0)

    print(f"\nThe server is running on {local_ip}")
    print("Share this IP address with the recipient")
    server.listen()

    print("\nWaiting for user to join...")

    while True:
        client, _ = server.accept()
        client_password = client.recv(1024).decode()

        if client_password == hashed:
            client.send("Password is correct. Joining...".encode())
            
            client.send(public_key.save_pkcs1("PEM")) # provides user with the partner's public key only if the password is correct !!
            public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
            print("Someone has joined the chat!")
            break
        else:
            client.send("Password is incorrect. Disconnecting".encode())
            client.close()
        

elif choice == "2": 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = input("Enter the host IP address: ")
    print("Attempting to connect...")
    client.connect((host_ip, PORT))
    print("\nConnected to host!")

    authentication = getpass.getpass("What is the password? ")
    hashed_attempt = sha256(authentication.encode()).hexdigest() # password attempt is hashed
    client.send(hashed_attempt.encode())


    response = client.recv(1024).decode()
    if "incorrect" in response:
        print(response)
        client.close()
        exit()
    else:
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024)) # only provides keys if password is correct (reversed order)
        client.send(public_key.save_pkcs1("PEM")) 
        print(response)

else:
    exit()

def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        # c.send(message.encode())
        print("You: " + message)

def recv_messages(c):
    while True:

        print("Them: " + rsa.decrypt(c.recv(1024), private_key).decode())
        # print("Them: " + c.recv(1024).decode())
 
threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=recv_messages, args=(client,)).start()
