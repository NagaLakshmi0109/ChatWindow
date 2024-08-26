#Socket programming - Server Program

import socket
import threading

HEADER = 64
PORT = 5096
SERVER = '138.68.140.83'
# SERVER= socket.gethostname()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} clientected.")
    clientected = True
    while clientected:
        msgLength = client.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = client.recv(msgLength).decode(FORMAT)
            if "bye" in msg:
                global clients
                clientected = False
                clientName = msg.split(':', 1)[0]
                print(clientName)
                broadcast(f"{clientName}has left the chat.".encode(FORMAT))
                clients.remove(client)
                client.close()
                print(f"[ACTIVE CONNECTECTION] {threading.activeCount() - 1}")
            else:
                message = f"{msg}".encode(FORMAT)
                broadcast(message)
    client.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        print(f"[ACTIVE CONNECTECTION] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()