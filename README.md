# e2ee-chat
A simple E2EE chat for 2 users over 1 network using python, with a basic authentication method

Project Scope:
My chat app will consist of a single server and a client, allowing 2 users to communicate in real time under the same network. The encryption algorithm used will be RSA, and it will follow a simple peer-to-peer setup (without a centralised server) for extra security. One user will first open the server and choose to host the chat, followed by creating a password (a shared secret that will be known to only both parties). The second user will choose to join the chat and will be prompted to enter the correct password, in order to join. 

The app follows several standards for a basic E2EE chat:
1. Each user has their own key pair generated
2. Only the public keys are shared across the network
3. Messages are encrypted with the other’s public key and decrypted using one’s private key
4. All messages are encrypted prior to transit, and remain encrypted until the recipient decrypts it with their private key
